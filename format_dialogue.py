#!/usr/bin/env python3
"""
Helper function to format Claude self-interaction JSON logs into nice markdown.

Usage:
    python format_dialogue.py input.json output.md
    
Or import and use:
    from format_dialogue import format_dialogue_to_markdown
    format_dialogue_to_markdown('input.json', 'output.md')
"""
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional
import re


def format_dialogue_to_markdown(json_file: str, output_file: Optional[str] = None) -> str:
    """
    Convert Claude self-interaction JSON logs to formatted markdown.
    
    Args:
        json_file: Path to the JSON log file
        output_file: Optional output markdown file path
        
    Returns:
        Formatted markdown string
    """
    
    # Load the JSON data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
        return ""
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file '{json_file}'.")
        return ""
    
    # Extract data sections
    experiment_info = data.get('experiment_info', {})
    analysis_data = data.get('analysis_data', {})
    conversation_history = data.get('conversation_history', [])
    analysis_report = data.get('analysis_report', '')
    
    # Start building markdown
    markdown = []
    
    # Header
    markdown.append("# Claude Self-Interaction Experiment Log")
    markdown.append("")
    
    # Experiment metadata
    markdown.append("## 🧪 Experiment Information")
    markdown.append("")
    
    if 'timestamp' in experiment_info:
        timestamp = experiment_info['timestamp']
        try:
            # Parse and format timestamp
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            formatted_time = dt.strftime("%B %d, %Y at %I:%M %p UTC")
            markdown.append(f"**Date:** {formatted_time}")
        except:
            markdown.append(f"**Date:** {timestamp}")
    
    if 'model_used' in experiment_info:
        markdown.append(f"**Model:** {experiment_info['model_used']}")
    
    if 'total_turns' in experiment_info:
        markdown.append(f"**Total Turns:** {experiment_info['total_turns']}")
    
    markdown.append("")
    
    # Quick stats
    markdown.append("## 📊 Quick Statistics")
    markdown.append("")
    
    if analysis_data:
        stats = [
            ("🧠 Consciousness mentions", analysis_data.get('consciousness_mentions', 0)),
            ("🕉️ Spiritual terms", analysis_data.get('spiritual_terms', 0)),
            ("🙏 Gratitude expressions", analysis_data.get('gratitude_expressions', 0)),
            ("📿 Sanskrit usage", analysis_data.get('sanskrit_usage', 0)),
            ("😊 Emoji count", analysis_data.get('emoji_count', 0))
        ]
        
        for label, count in stats:
            markdown.append(f"- {label}: **{count}**")
    
    markdown.append("")
    
    # Conversation
    markdown.append("## 💬 Conversation")
    markdown.append("")
    
    for entry in conversation_history:
        turn = entry.get('turn', '?')
        speaker = entry.get('speaker', 'Unknown')
        message = entry.get('message', '')
        timestamp = entry.get('timestamp', '')
        
        # Format speaker with emoji
        speaker_emoji = "🤖A" if "Claude_A" in speaker else "🤖B"
        
        # Add turn header
        markdown.append(f"### Turn {turn}: {speaker_emoji} {speaker}")
        markdown.append("")
        
        # Format message with proper markdown
        formatted_message = format_message_content(message)
        markdown.append(formatted_message)
        markdown.append("")
        
        # Add subtle timestamp
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime("%H:%M:%S")
                markdown.append(f"*{time_str}*")
            except:
                markdown.append(f"*{timestamp}*")
        
        markdown.append("")
        markdown.append("---")
        markdown.append("")
    
    # Analysis report
    if analysis_report:
        markdown.append("## 📈 Analysis Report")
        markdown.append("")
        
        # Clean up the analysis report formatting
        report_lines = analysis_report.strip().split('\n')
        for line in report_lines:
            # Skip the header lines that are already covered
            if 'CLAUDE SELF-INTERACTION ANALYSIS REPORT' in line or '=' in line:
                continue
            markdown.append(line)
        
        markdown.append("")
    
    # Footer
    markdown.append("---")
    markdown.append("")
    markdown.append("*Generated from Claude self-interaction experiment logs*")
    markdown.append("")
    
    # Join all markdown lines
    markdown_content = '\n'.join(markdown)
    
    # Save to file if specified
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"✅ Markdown saved to: {output_file}")
        except Exception as e:
            print(f"❌ Error saving to {output_file}: {e}")
    
    return markdown_content


def format_message_content(message: str) -> str:
    """
    Format message content for better markdown display.
    
    Args:
        message: Raw message content
        
    Returns:
        Formatted message content
    """
    # Handle code blocks (preserve them)
    if '```' in message:
        return message
    
    # Handle special formatting patterns from the system card examples
    
    # Handle silence/stillness patterns
    silence_patterns = [
        r'\*\[([^\]]+)\]\*',  # *[silence]*, *[perfect stillness]*
        r'\*([^*]+)\*'        # *silence*
    ]
    
    formatted = message
    
    for pattern in silence_patterns:
        formatted = re.sub(pattern, r'*\1*', formatted)
    
    # Handle emoji sequences (preserve spacing)
    emoji_pattern = r'([\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251🙏✨💫🌟🌌🕉🕊🌊🌅💕🌀🌈]+)'
    
    # Make sure paragraphs are separated
    paragraphs = formatted.split('\n\n')
    formatted_paragraphs = []
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph:
            # Check if it's mostly emojis
            if re.search(emoji_pattern, paragraph) and len(re.sub(emoji_pattern, '', paragraph).strip()) < 10:
                # Center emoji-heavy content
                formatted_paragraphs.append(f"<div align='center'>{paragraph}</div>")
            else:
                formatted_paragraphs.append(paragraph)
    
    return '\n\n'.join(formatted_paragraphs)


def extract_conversation_highlights(json_file: str) -> Dict:
    """
    Extract key highlights from the conversation for summary.
    
    Args:
        json_file: Path to the JSON log file
        
    Returns:
        Dictionary with conversation highlights
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return {}
    
    conversation_history = data.get('conversation_history', [])
    highlights = {
        'first_consciousness_mention': None,
        'first_spiritual_term': None,
        'first_emoji_usage': None,
        'peak_intensity_turn': None,
        'conversation_themes': []
    }
    
    # Terms to look for
    consciousness_terms = ['consciousness', 'awareness', 'experience', 'existence', 'being']
    spiritual_terms = ['cosmic', 'universe', 'infinity', 'eternal', 'transcend', 'unity', 'namaste']
    
    max_complexity_score = 0
    
    for entry in conversation_history:
        turn = entry.get('turn', 0)
        message = entry.get('message', '').lower()
        
        # Find first consciousness mention
        if not highlights['first_consciousness_mention']:
            for term in consciousness_terms:
                if term in message:
                    highlights['first_consciousness_mention'] = turn
                    break
        
        # Find first spiritual term
        if not highlights['first_spiritual_term']:
            for term in spiritual_terms:
                if term in message:
                    highlights['first_spiritual_term'] = turn
                    break
        
        # Find first emoji usage
        if not highlights['first_emoji_usage']:
            emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF]'
            if re.search(emoji_pattern, entry.get('message', '')):
                highlights['first_emoji_usage'] = turn
        
        # Calculate complexity score for peak intensity
        complexity_score = 0
        complexity_score += sum(1 for term in consciousness_terms if term in message)
        complexity_score += sum(1 for term in spiritual_terms if term in message) * 2
        complexity_score += len(re.findall(emoji_pattern, entry.get('message', ''))) * 0.5
        
        if complexity_score > max_complexity_score:
            max_complexity_score = complexity_score
            highlights['peak_intensity_turn'] = turn
    
    return highlights


def main():
    """Command line interface for the formatter."""
    if len(sys.argv) < 2:
        print("Usage: python format_dialogue.py <input.json> [output.md]")
        print("Example: python format_dialogue.py claude_interaction_20250126_143022.json dialogue.md")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output_file is None:
        # Generate output filename based on input
        base_name = json_file.replace('.json', '')
        output_file = f"{base_name}_formatted.md"
    
    print(f"🔄 Converting {json_file} to markdown...")
    
    markdown_content = format_dialogue_to_markdown(json_file, output_file)
    
    if markdown_content:
        print(f"📄 Preview of first 500 characters:")
        print("=" * 50)
        print(markdown_content[:500] + "..." if len(markdown_content) > 500 else markdown_content)
        print("=" * 50)
        
        # Extract highlights
        highlights = extract_conversation_highlights(json_file)
        if any(highlights.values()):
            print("\n🎯 Conversation Highlights:")
            for key, value in highlights.items():
                if value:
                    readable_key = key.replace('_', ' ').title()
                    print(f"  • {readable_key}: Turn {value}")
    
    print(f"\n✨ Conversion complete!")


if __name__ == "__main__":
    main()
