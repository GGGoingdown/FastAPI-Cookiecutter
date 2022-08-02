import sys
import traceback
from pathlib import Path
from tortoise import Tortoise, run_async
from tenacity import retry, stop_after_attempt, wait_fixed
from loguru import logger

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # app folder
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH


###
from app.containers import Application  # noqa: E402

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(stop=stop_after_attempt(max_tries), wait=wait_fixed(wait_seconds))
async def db_connected():
    try:
        conn = Tortoise.get_connection("default")
        logger.info(f"Ping -> {await conn.execute_query('SELECT 1')}")

    except ConnectionRefusedError as e:
        error_message = traceback.format_exc()
        logger.error(error_message)
        raise e

    except Exception as e:
        error_message = traceback.format_exc()
        logger.error(error_message)
        raise e


async def main():
    try:
        container = Application()
        logger.info("--- Connect DB ---")
        await container.gateway.db_resource.init()
        await db_connected()

    finally:
        await container.gateway.db_resource.shutdown()


if __name__ == "__main__":
    run_async(main())
