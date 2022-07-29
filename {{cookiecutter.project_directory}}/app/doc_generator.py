from app import create_app, __VERSION__, __TITLE__

app = create_app()

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>LiveBroadcast</title>
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
        Redoc.init(spec, {}, document.getElementById("redoc-container"));
    </script>
</body>
</html>
"""


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    documents_folder = Path("docs")

    if not documents_folder.is_dir():
        documents_folder.mkdir()

    parser = argparse.ArgumentParser(description="Run celery or Document generator")
    parser.add_argument("--celery", type=bool, default=False, help="Run celery")
    parser.add_argument(
        "--doc", type=bool, default=False, help="Run document generator"
    )
    args = parser.parse_args()
    if args.doc:
        print("--- Document ---")
        import json

        version = __VERSION__.replace(".", "")
        file_name = "-".join(__TITLE__.lower().split(" "))
        full_file_name = f"api-docs-{file_name}_v{version}"
        with open(f"./docs/{full_file_name}.html", "w") as fd:
            print(HTML_TEMPLATE % json.dumps(app.openapi()), file=fd)

        with open(f"./docs/{full_file_name}.json", "w") as fd:
            print(json.dumps(app.openapi()), file=fd)
