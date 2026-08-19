#!/usr/bin/env python3
"""
Quick PDF generator for OpenClaw as an AI Agentic OS
Produces a review-only PDF from paper.md (not IEEE two-column format).

For the official IEEE two-column submission PDF, use LaTeX:
    pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex

Usage:
    pip install markdown weasyprint
    python3 generate_pdf.py
"""

import os
import sys

def check_dependencies():
    missing = []
    try:
        import markdown
    except ImportError:
        missing.append("markdown")
    try:
        import weasyprint
    except ImportError:
        missing.append("weasyprint")
    if missing:
        print(f"Missing dependencies. Install with:")
        print(f"  pip install {' '.join(missing)}")
        sys.exit(1)

def generate():
    check_dependencies()
    import markdown
    from weasyprint import HTML, CSS

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "paper.md")
    output_path = os.path.join(script_dir, "paper_review.pdf")

    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_body = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "toc"]
    )

    css = CSS(string="""
        @page {
            size: A4;
            margin: 2.5cm 2.5cm 2.5cm 2.5cm;
        }
        body {
            font-family: "Times New Roman", Times, serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #000;
        }
        h1 {
            font-size: 16pt;
            font-weight: bold;
            text-align: center;
            margin-top: 0;
            margin-bottom: 6pt;
        }
        h2 {
            font-size: 13pt;
            font-weight: bold;
            margin-top: 14pt;
            margin-bottom: 4pt;
            border-bottom: 1px solid #000;
            padding-bottom: 2pt;
        }
        h3 {
            font-size: 11pt;
            font-weight: bold;
            font-style: italic;
            margin-top: 10pt;
            margin-bottom: 2pt;
        }
        p {
            margin: 6pt 0;
            text-align: justify;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 10pt 0;
            font-size: 9pt;
        }
        th {
            background-color: #f0f0f0;
            border: 1px solid #999;
            padding: 4pt 6pt;
            font-weight: bold;
            text-align: left;
        }
        td {
            border: 1px solid #ccc;
            padding: 3pt 6pt;
            vertical-align: top;
        }
        code {
            font-family: "Courier New", monospace;
            font-size: 9pt;
            background-color: #f5f5f5;
            padding: 1pt 3pt;
            border-radius: 2pt;
        }
        pre {
            font-family: "Courier New", monospace;
            font-size: 8.5pt;
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            padding: 8pt;
            margin: 8pt 0;
            white-space: pre-wrap;
            word-wrap: break-word;
            border-radius: 3pt;
        }
        blockquote {
            border-left: 3pt solid #666;
            margin: 8pt 0 8pt 16pt;
            padding-left: 8pt;
            font-style: italic;
            color: #333;
        }
        ul, ol {
            margin: 6pt 0;
            padding-left: 20pt;
        }
        li {
            margin-bottom: 3pt;
        }
        hr {
            border: none;
            border-top: 1px solid #ccc;
            margin: 14pt 0;
        }
        strong {
            font-weight: bold;
        }
        em {
            font-style: italic;
        }
    """)

    html_full = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>OpenClaw as an AI Agentic OS</title>
</head>
<body>
{html_body}
</body>
</html>"""

    HTML(string=html_full, base_url=script_dir).write_pdf(
        output_path, stylesheets=[css]
    )
    print(f"Review PDF generated: {output_path}")
    print()
    print("NOTE: This is a review-only PDF. For IEEE two-column submission:")
    print("  pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex")

if __name__ == "__main__":
    generate()
