"""Convert Startup_Validation_Report.md to clean HTML and PDF."""
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
MD_FILE = ROOT / "Startup_Validation_Report.md"
HTML_FILE = ROOT / "Startup_Validation_Report.html"
PDF_FILE = ROOT / "Startup_Validation_Report.pdf"

A4_WIDTH = 794
A4_HEIGHT = 1123

CSS = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }

*, *::before, *::after { box-sizing: border-box; }

html {
    -webkit-text-size-adjust: 100%;
    text-size-adjust: 100%;
}

body {
    font-family: "Segoe UI", Calibri, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.55;
    color: #1a1a2e;
    margin: 0 auto;
    padding: 24px 32px 48px;
    max-width: 210mm;
    min-width: 680px;
    word-break: normal;
    overflow-wrap: break-word;
    hyphens: manual;
}

h1 {
    font-size: 24pt;
    color: #0f3460;
    border-bottom: 3px solid #0f3460;
    padding-bottom: 10px;
    margin: 0 0 20px;
}
h2 {
    font-size: 15pt;
    color: #16213e;
    border-bottom: 2px solid #e94560;
    padding-bottom: 6px;
    margin: 32px 0 14px;
    page-break-after: avoid;
}
h3 {
    font-size: 12pt;
    color: #0f3460;
    margin: 20px 0 10px;
    page-break-after: avoid;
}
h4 { font-size: 11pt; margin: 16px 0 8px; }

p { margin: 0 0 12px; }
strong { font-weight: 700; }
em { font-style: italic; }

a { color: #0f3460; text-decoration: none; }

hr {
    border: none;
    border-top: 1px solid #c8d0da;
    margin: 28px 0;
}

ul, ol {
    margin: 8px 0 14px 24px;
    padding: 0;
}
li { margin-bottom: 6px; }

/* ── Tables ── */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 20px;
    font-size: 10pt;
    table-layout: fixed;
    page-break-inside: avoid;
}

th, td {
    border: 1px solid #c8d0da;
    padding: 8px 10px;
    text-align: left;
    vertical-align: top;
    word-break: normal;
    overflow-wrap: break-word;
    white-space: normal;
    line-height: 1.45;
}

th {
    background: #0f3460;
    color: #fff;
    font-weight: 700;
    border-color: #0f3460;
}

tbody tr:nth-child(even) td { background: #f4f7fb; }

/* 2-column key/value */
table.cols-2 th:nth-child(1), table.cols-2 td:nth-child(1) { width: 30%; }
table.cols-2 th:nth-child(2), table.cols-2 td:nth-child(2) { width: 70%; }

/* 3-column */
table.cols-3 th, table.cols-3 td { width: 33.33%; font-size: 9.5pt; }

/* 4-column */
table.cols-4 th, table.cols-4 td { width: 25%; font-size: 9pt; }

/* 5-column */
table.cols-5 th, table.cols-5 td { width: 20%; font-size: 8.5pt; }

/* 6-column */
table.cols-6 th, table.cols-6 td { width: 16.66%; font-size: 8pt; }

/* 7-column (competitor table) */
table.cols-7 th, table.cols-7 td { width: 14.28%; font-size: 7.5pt; padding: 5px 6px; }

/* Scorecard */
table.scorecard th { text-align: center; }
table.scorecard td:nth-child(1) { width: 38%; }
table.scorecard td:nth-child(2) { width: 32%; }
table.scorecard td:nth-child(3) { width: 30%; }
table.scorecard .total td {
    background: #dce6f2;
    font-weight: 700;
    text-align: center;
}

/* Flow / journey table */
table.flow-table th { text-align: center; font-size: 9pt; }
table.flow-table td { text-align: center; font-size: 9pt; }

blockquote {
    border-left: 4px solid #e94560;
    margin: 14px 0;
    padding: 10px 16px;
    background: #fdf2f4;
    color: #333;
}

/* Recommendation box */
.recommendation-box {
    border: 3px solid #0f3460;
    border-radius: 6px;
    background: #eef3fa;
    padding: 20px 24px;
    margin: 18px 0 24px;
    text-align: center;
}
.recommendation-box .verdict {
    font-size: 18pt;
    font-weight: 700;
    color: #0f3460;
    margin: 10px 0;
}

.cover-title {
    text-align: center;
    margin-bottom: 8px;
}
.cover-title h1 {
    border-bottom: none;
    font-size: 28pt;
    margin-bottom: 4px;
}

.section-break { page-break-before: always; }

.footer-note {
    margin-top: 48px;
    padding-top: 14px;
    border-top: 1px solid #c8d0da;
    font-size: 9pt;
    color: #777;
    text-align: center;
}
"""


def count_columns(table_html: str) -> int:
    thead = re.search(r"<thead>.*?</thead>", table_html, re.DOTALL)
    if thead:
        return len(re.findall(r"<th[\s>]", thead.group(0)))
    first_row = re.search(r"<tr>(.*?)</tr>", table_html, re.DOTALL)
    if first_row:
        row = first_row.group(1)
        n = len(re.findall(r"<th[\s>]", row))
        return n if n else len(re.findall(r"<td[\s>]", row))
    return 2


def tag_tables(html: str) -> str:
    def replacer(match: re.Match) -> str:
        table = match.group(0)
        if re.search(r"<table[^>]+class=", table):
            return table
        cols = count_columns(table)
        cls = f"cols-{min(max(cols, 2), 7)}"
        if "Field" in table and cols == 2:
            cls += " meta-table"
        return table.replace("<table>", f'<table class="{cls}">', 1)

    return re.sub(r"<table>.*?</table>", replacer, html, flags=re.DOTALL)


def md_to_html(md_text: str) -> str:
    body = markdown.markdown(
        md_text,
        extensions=["tables", "sane_lists", "nl2br"],
    )
    body = tag_tables(body)
    body = body.replace(
        "<h2>1. EXECUTIVE SUMMARY</h2>",
        '<h2 class="section-break">1. EXECUTIVE SUMMARY</h2>',
    )

    if "</h1>" in body:
        title_part, rest = body.split("</h1>", 1)
        cover = f'<div class="cover-title">{title_part}</h1></div>'
        body = cover + rest

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width={A4_WIDTH}, initial-scale=1.0"/>
<title>Startup Validation Report — NightShift Kitchen</title>
<style>{CSS}</style>
</head>
<body>
{body}
<div class="footer-note">Startup Validation Report — Confidential — NightShift Kitchen</div>
</body>
</html>"""


def html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": A4_WIDTH, "height": A4_HEIGHT})
        page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
        page.emulate_media(media="print")
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "18mm", "right": "16mm", "bottom": "20mm", "left": "16mm"},
        )
        browser.close()


def main() -> None:
    md_text = MD_FILE.read_text(encoding="utf-8")
    html = md_to_html(md_text)
    HTML_FILE.write_text(html, encoding="utf-8")

    target = PDF_FILE
    try:
        html_to_pdf(HTML_FILE, target)
    except PermissionError:
        target = ROOT / "Startup_Validation_Report_v4.pdf"
        html_to_pdf(HTML_FILE, target)

    print(f"HTML: {HTML_FILE}")
    print(f"PDF:  {target} ({target.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
