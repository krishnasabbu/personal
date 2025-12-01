import fitz  # PyMuPDF

def pdf_to_html(pdf_path, html_path):
    doc = fitz.open(pdf_path)

    html_content = """
    <html>
    <head>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }
        .page {
            background: white;
            padding: 20px;
            margin-bottom: 40px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        img {
            max-width: 100%;
            display: block;
        }
    </style>
    </head>
    <body>
    """

    for i, page in enumerate(doc):
        xhtml = page.get_text("xhtml")   # <-- FIX: Use XHTML instead of HTML
        html_content += f'<div class="page">{xhtml}</div>\n'

    html_content += "</body></html>"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✔ PDF → HTML fixed (no overlapping images):", html_path)


pdf_to_html("input.pdf", "output.html")