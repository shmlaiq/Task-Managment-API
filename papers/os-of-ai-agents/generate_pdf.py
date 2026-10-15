"""
generate_pdf.py — Quick PDF generator for AgentOS paper (review format only).

For REVIEW only — does NOT produce IEEE two-column layout.
For official IEEE submission use:
    pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex

Requirements:
    pip install markdown weasyprint
    OR
    pip install markdown reportlab

Usage:
    python3 generate_pdf.py
"""

import os
import sys

PAPER_MD = "paper.md"
OUTPUT_PDF = "paper_review.pdf"


def generate_with_weasyprint():
    """Generate PDF via Markdown -> HTML -> PDF (requires weasyprint)."""
    import markdown
    from weasyprint import HTML, CSS

    with open(PAPER_MD, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "toc"]
    )

    html_page = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    font-family: "Times New Roman", Times, serif;
    font-size: 12pt;
    line-height: 1.6;
    margin: 2.5cm 2.5cm 2.5cm 2.5cm;
    color: #000;
  }}
  h1 {{ font-size: 16pt; text-align: center; margin-bottom: 0.3em; }}
  h2 {{ font-size: 13pt; margin-top: 1.4em; border-bottom: 1px solid #ccc; }}
  h3 {{ font-size: 12pt; margin-top: 1em; }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 10pt;
  }}
  th, td {{
    border: 1px solid #555;
    padding: 4px 8px;
    text-align: left;
  }}
  th {{ background: #eee; font-weight: bold; }}
  code, pre {{
    font-family: "Courier New", monospace;
    font-size: 9pt;
    background: #f5f5f5;
    padding: 2px 4px;
  }}
  pre {{ padding: 0.8em; border: 1px solid #ddd; }}
  blockquote {{
    border-left: 3px solid #aaa;
    margin-left: 0;
    padding-left: 1em;
    color: #555;
  }}
  @page {{
    margin: 2.5cm;
    @bottom-center {{
      content: counter(page);
    }}
  }}
</style>
</head>
<body>
{html_content}
</body>
</html>"""

    HTML(string=html_page).write_pdf(
        OUTPUT_PDF,
        stylesheets=[CSS(string="body { font-size: 12pt; }")]
    )
    print(f"[OK] PDF generated: {OUTPUT_PDF}")
    print("     (Review format — NOT IEEE two-column)")


def generate_with_reportlab():
    """Fallback: plain-text PDF via reportlab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
    from reportlab.lib.enums import TA_LEFT, TA_CENTER

    with open(PAPER_MD, "r", encoding="utf-8") as f:
        lines = f.readlines()

    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        rightMargin=2.5 * cm,
        leftMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("Title", parent=styles["Title"],
                                  fontSize=14, spaceAfter=12, alignment=TA_CENTER)
    h1_style = ParagraphStyle("H1", parent=styles["Heading1"],
                               fontSize=13, spaceBefore=12, spaceAfter=6)
    h2_style = ParagraphStyle("H2", parent=styles["Heading2"],
                               fontSize=12, spaceBefore=10, spaceAfter=4)
    h3_style = ParagraphStyle("H3", parent=styles["Heading3"],
                               fontSize=11, spaceBefore=8, spaceAfter=3)
    body_style = ParagraphStyle("Body", parent=styles["Normal"],
                                 fontSize=11, spaceAfter=6, leading=15)
    code_style = ParagraphStyle("Code", parent=styles["Code"],
                                 fontSize=8, fontName="Courier", spaceAfter=6)

    story = []
    first_h1 = True

    for line in lines:
        line = line.rstrip("\n")
        if line.startswith("# ") and first_h1:
            story.append(Paragraph(line[2:], title_style))
            first_h1 = False
        elif line.startswith("## "):
            story.append(Spacer(1, 6))
            story.append(Paragraph(line[3:], h1_style))
        elif line.startswith("### "):
            story.append(Paragraph(line[4:], h2_style))
        elif line.startswith("#### "):
            story.append(Paragraph(line[5:], h3_style))
        elif line.startswith("```"):
            pass  # skip fence markers
        elif line.startswith("    ") or line.startswith("\t"):
            story.append(Preformatted(line, code_style))
        elif line.strip() == "":
            story.append(Spacer(1, 4))
        else:
            # strip markdown bold/italic for plain text
            text = line.replace("**", "").replace("*", "").replace("`", "")
            story.append(Paragraph(text, body_style))

    doc.build(story)
    print(f"[OK] PDF generated (fallback mode): {OUTPUT_PDF}")
    print("     (Plain-text layout — NOT IEEE two-column)")


def main():
    if not os.path.exists(PAPER_MD):
        print(f"[ERROR] {PAPER_MD} not found. Run from the paper directory.")
        sys.exit(1)

    print("Attempting PDF generation...")
    print()

    # Try weasyprint first (better output)
    try:
        import markdown  # noqa
        import weasyprint  # noqa
        generate_with_weasyprint()
        return
    except ImportError:
        print("[INFO] weasyprint not found. Trying reportlab...")

    # Fallback: reportlab
    try:
        import reportlab  # noqa
        generate_with_reportlab()
        return
    except ImportError:
        pass

    # Neither library available
    print("[ERROR] No PDF library found.")
    print()
    print("Install one of the following:")
    print("  pip install markdown weasyprint     (recommended)")
    print("  pip install reportlab               (fallback)")
    print()
    print("For official IEEE submission (two-column layout), use LaTeX:")
    print("  pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex")
    sys.exit(1)


if __name__ == "__main__":
    main()
