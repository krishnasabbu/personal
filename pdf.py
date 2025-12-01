import fitz
import base64

def pdf_to_html_fixed(pdf_path, html_path):
    doc = fitz.open(pdf_path)

    html_content = """
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }
        .page {
            background: white;
            padding: 20px;
            margin: 40px auto;
            max-width: 900px;
            box-shadow: 0 0 10px rgba(0,0,0,0.15);
        }
        img {
            max-width: 100%;
            display: block;
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        td, th {
            border: 1px solid #ccc;
            padding: 4px 6px;
        }
    </style>
    </head>
    <body>
    """

    for page_index, page in enumerate(doc):

        # Extract XHTML
        xhtml = page.get_text("xhtml")

        # Extract image blocks from layout
        blocks = page.get_text("dict")["blocks"]

        img_counter = 0

        for b in blocks:
            if b["type"] == 1:  # Image block
                img_counter += 1

                # Render exact image region
                pix = page.get_pixmap(clip=b["bbox"], dpi=150)

                # Convert to Base64
                img_bytes = pix.tobytes("png")
                b64 = base64.b64encode(img_bytes).decode("utf-8")

                # Replace image tag sequentially
                xhtml = xhtml.replace(
                    f"src=\"{img_counter}\"",
                    f"src=\"data:image/png;base64,{b64}\""
                )

        html_content += f"<div class='page'>{xhtml}</div>"

    html_content += "</body></html>"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✔ Fixed HTML created with perfectly rendered images:", html_path)