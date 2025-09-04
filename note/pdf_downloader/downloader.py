import pdfkit

def download_pdf_html_strings(html_content: str):
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <link rel="stylesheet" href="https://cdn.quilljs.com/1.3.6/quill.snow.css">
            <link rel="stylesheet" href="http://localhost:5173/src/index.css">
        </head>

        <body>
            {html_content}
        </body>
        </html>
        """


def download_pdf(name: str, html_content: str, user_id: str):
    try:
        full_html = download_pdf_html_strings(html_content=html_content)
        options = {
            "enable-local-file-access": None,
            "encoding": "UTF-8",
        }
        data = pdfkit.from_string(full_html, False, options=options)
        content_type="application/pdf"
        file_name = f"{name}_{user_id}_output.pdf"
        return data, content_type, file_name
    except (ValueError, TypeError) as e:
        return e