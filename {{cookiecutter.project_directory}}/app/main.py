try:
    from app import create_app
except ModuleNotFoundError:
    import sys
    from pathlib import Path

    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[1]  # app folder
    if str(ROOT) not in sys.path:
        sys.path.append(str(ROOT))  # add ROOT to PATH

    from app import create_app

app = create_app()
celery = app.celery_app


def run_worker():
    import subprocess

    subprocess.call(
        [
            "celery",
            "-A",
            "app.main.celery",
            "worker",
            "-c",
            "1",
            "--loglevel=info",
            "-E",
            "--without-heartbeat",
            "--without-gossip",
            "--without-mingle",
            "-Ofair",
        ]
    )


def celery_watchgod():
    from watchgod import run_process

    run_process("./app", run_worker)


if __name__ == "__main__":
    celery_watchgod()
