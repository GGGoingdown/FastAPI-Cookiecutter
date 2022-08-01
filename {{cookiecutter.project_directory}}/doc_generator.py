from app import create_app, __VERSION__, __TITLE__

app = create_app()

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>%s</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    <style>
        body {
            margin: 0;
            padding: 0;
        }
    </style>
    <style data-styled="" data-styled-version="4.4.1"></style>
</head>
<body>
    <div id="redoc-container"></div>
    <script src="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"> </script>
    <script>
        var spec = %s;
        Redoc.init(spec, '{}', document.getElementById("redoc-container"));
    </script>
</body>
</html>
"""


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Run celery or Document generator")
    parser.add_argument(
        "--remove-old", type=bool, default=True, help="Remove old version documents"
    )
    args = parser.parse_args()

    # Check docs folder
    documents_folder = Path("docs")
    print(f"--- Document {documents_folder}---")
    if not documents_folder.is_dir():
        documents_folder.mkdir()

    if args.remove_old:
        print("--- Remove old version documents ---")
        for doc_path in documents_folder.iterdir():
            if doc_path.is_file():
                print(f"Remove file: {doc_path}")
                doc_path.unlink()

    version = __VERSION__.replace(".", "")
    file_name = "-".join(__TITLE__.lower().split(" "))
    html_title = __TITLE__.capitalize()
    full_file_name = f"api-docs-{file_name}_v{version}"
    with open(f"./docs/{full_file_name}.html", "w") as fd:
        print(HTML_TEMPLATE % (html_title, json.dumps(app.openapi())), file=fd)

    with open(f"./docs/{full_file_name}.json", "w") as fd:
        print(json.dumps(app.openapi()), file=fd)
