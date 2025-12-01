import fitz
import base64

def pdf_to_single_html(pdf_path, html_path):
    doc = fitz.open(pdf_path)

    # HTML + CSS
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
            background: #fff;
            padding: 20px;
            margin: 40px auto;
            max-width: 900px;
            box-shadow: 0 0 10px rgba(0,0,0,0.15);
        }
        img {
            max-width: 100%;
            display: block;
        }
        /* Table alignment improvements */
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

        # Extract XHTML (best structured output)
        xhtml = page.get_text("xhtml")

        # --- EMBED IMAGES AS BASE64 ---
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]

            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]
            img_ext   = base_image["ext"]

            b64 = base64.b64encode(img_bytes).decode()

            # Replace image reference inside XHTML with embedded base64
            xhtml = xhtml.replace(
                f"src=\"{xref}\"",
                f"src=\"data:image/{img_ext};base64,{b64}\""
            )

        # Add page wrapper
        html_content += f"<div class='page'>{xhtml}</div>\n"

    html_content += "</body></html>"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✔ DONE! All pages embedded with base64 images:")
    print("→", html_path)


# RUN
pdf_to_single_html("input.pdf", "output.html")