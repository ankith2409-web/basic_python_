import re

def parse_markdown(md_text):
    """
    A simple markdown to HTML converter supporting headers, bold, italics, and unordered lists.
    """
    # Headers
    html_text = re.sub(r'^### (.*)$', r'<h3>\1</h3>', md_text, flags=re.MULTILINE)
    html_text = re.sub(r'^## (.*)$', r'<h2>\1</h2>', html_text, flags=re.MULTILINE)
    html_text = re.sub(r'^# (.*)$', r'<h1>\1</h1>', html_text, flags=re.MULTILINE)
    
    # Bold
    html_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_text)
    
    # Italics
    html_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_text)
    
    # Unordered Lists
    def list_replacer(match):
        items = match.group(0).strip().split('\n')
        list_html = "<ul>\n"
        for item in items:
            list_html += f"  <li>{item.strip()[2:]}</li>\n"
        list_html += "</ul>"
        return list_html

    html_text = re.sub(r'(?:^- .*(?:\n|$))+', list_replacer, html_text, flags=re.MULTILINE)
    
    # Paragraphs (basic approach)
    paragraphs = []
    for line in html_text.split('\n'):
        line = line.strip()
        if not line:
            continue
        if not line.startswith('<'):
            line = f"<p>{line}</p>"
        paragraphs.append(line)
        
    return "\n".join(paragraphs)

if __name__ == "__main__":
    sample_md = """# My Document
## Introduction
This is a **bold** word and an *italic* word.
- Item 1
- Item 2
- Item 3

This is a new paragraph."""
    
    print("--- Original Markdown ---\n")
    print(sample_md)
    print("\n--- Converted HTML ---\n")
    print(parse_markdown(sample_md))
