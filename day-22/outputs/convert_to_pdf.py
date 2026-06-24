"""Convert Startup_Validation_Report.md to a styled PDF via Playwright."""
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
MD_FILE = ROOT / "Startup_Validation_Report.md"
PDF_FILE = ROOT / "Startup_Validation_Report.pdf"
HTML_FILE = ROOT / "Startup_Validation_Report.html"

CSS = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
* { box-sizing: border-box; }
body {
    font-family: "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.5;
    color: #1a1a2e;
    max-width: 100%;
    margin: 0;
    padding: 0;
}
h1 {
    font-size: 22pt;
    color: #0f3460;
    border-bottom: 3px solid #0f3460;
    padding-bottom: 8px;
    margin: 0 0 16px 0;
    page-break-after: avoid;
}
h2 {
    font-size: 14pt;
    color: #16213e;
    border-bottom: 1px solid #e94560;
    padding-bottom: 4px;
    margin: 28px 0 12px 0;
    page-break-after: avoid;
}
h3 {
    font-size: 11pt;
    color: #0f3460;
    margin: 18px 0 8px 0;
    page-break-after: avoid;
}
h4 { font-size: 10pt; color: #333; margin: 14px 0 6px 0; }
p { margin: 0 0 10px 0; }
table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 18px 0;
    font-size: 9.5pt;
    table-layout: fixed;
    page-break-inside: avoid;
}
th {
    background-color: #0f3460;
    color: #ffffff;
    font-weight: bold;
    padding: 8px 10px;
    text-align: left;
    border: 1px solid #0f3460;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
td {
    padding: 7px 10px;
    border: 1px solid #d0d7de;
    vertical-align: top;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
/* Two-column tables: label column narrower */
table tr td:first-child,
table tr th:first-child {
    width: 28%;
}
table tr td:last-child,
table tr th:last-child {
    width: 72%;
}
/* Three+ column tables: equal-ish distribution */
table.cols-3 th, table.cols-3 td { width: 33.33%; }
table.cols-4 th, table.cols-4 td { width: 25%; }
table.cols-5 th, table.cols-5 td { width: 20%; }
tr:nth-child(even) td { background-color: #f6f8fa; }
blockquote {
    border-left: 4px solid #e94560;
    margin: 12px 0;
    padding: 8px 14px;
    background: #fdf2f4;
    font-style: italic;
    color: #333;
}
pre {
    font-family: Consolas, "Courier New", monospace;
    font-size: 7.5pt;
    background: #f4f4f8;
    border: 1px solid #ddd;
    padding: 10px 12px;
    white-space: pre-wrap;
    word-wrap: break-word;
    overflow-wrap: break-word;
    line-height: 1.35;
    margin: 10px 0 14px 0;
    page-break-inside: avoid;
}
code {
    font-family: Consolas, "Courier New", monospace;
    font-size: 9pt;
    background: #f0f0f5;
    padding: 1px 4px;
}
hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 24px 0;
}
ul, ol { margin: 8px 0 12px 22px; }
li { margin-bottom: 4px; }
a { color: #0f3460; text-decoration: none; }
.section-break { page-break-before: always; }
.cover-block {
    text-align: center;
    margin-bottom: 24px;
}
.cover-block h1 {
    border-bottom: none;
    font-size: 26pt;
    margin-bottom: 8px;
}
.footer-note {
    margin-top: 40px;
    padding-top: 12px;
    border-top: 1px solid #ccc;
    font-size: 8.5pt;
    color: #888;
    text-align: center;
}
"""


def tag_tables(html: str) -> str:
    """Add column-count classes so wide tables get sensible widths."""
    import re

    def replacer(match: re.Match) -> str:
        table = match.group(0)
        header = re.search(r"<thead>.*?</thead>", table, re.DOTALL)
        if not header:
            first_row = re.search(r"<tr>(.*?)</tr>", table, re.DOTALL)
            if not first_row:
                return table
            cols = first_row.group(1).count("<th>") or first_row.group(1).count("<td>")
        else:
            cols = header.group(0).count("<th>")
        if 3 <= cols <= 6:
            return table.replace("<table>", f'<table class="cols-{cols}">', 1)
        return table

    return re.sub(r"<table>.*?</table>", replacer, html, flags=re.DOTALL)


def md_to_html(md_text: str) -> str:
    extensions = ["tables", "fenced_code", "sane_lists"]
    body = markdown.markdown(md_text, extensions=extensions)
    body = tag_tables(body)
    # Section breaks before numbered h2 sections (not TOC)
    body = body.replace("<h2>1. EXECUTIVE SUMMARY</h2>", '<h2 class="section-break">1. EXECUTIVE SUMMARY</h2>')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Startup Validation Report</title>
<style>{CSS}</style>
</head>
<body>
<div class="cover-block">
{body.split("</h1>", 1)[0]}</h1>
</div>
{body.split("</h1>", 1)[1]}
<div class="footer-note">Startup Validation Report — Confidential</div>
</body>
</html>"""


def html_to_pdf_playwright(html_path: Path, pdf_path: Path) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "18mm", "right": "16mm", "bottom": "20mm", "left": "16mm"},
        )
        browser.close()


def main() -> None:
    md_text = MD_FILE.read_text(encoding="utf-8")
    html = md_to_html(md_text)
    HTML_FILE.write_text(html, encoding="utf-8")
    html_to_pdf_playwright(HTML_FILE, PDF_FILE)
    size_kb = PDF_FILE.stat().st_size // 1024
    print(f"Created: {PDF_FILE}")
    print(f"Size: {size_kb} KB")


if __name__ == "__main__":
    main()
