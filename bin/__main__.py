import argparse
import asyncio
import logging
import os
import sys

import uvicorn
from src.main import app
from src.core.config import settings
from src.db.sqlalch.core import init_models
from src.core.logs import configure_log


logger = logging.getLogger()


async def run() -> None:
    try:
        server = uvicorn.Server(
            config=uvicorn.Config(
                app=app,
                host=settings.project_host,
                port=settings.project_port,
            )
        )
        await server.serve()
    except asyncio.CancelledError:
        logger.info("HTTP server has been interrupted")
    except BaseException as unexpected_error:
        logger.exception("HTTP server failed to start", exc_info=unexpected_error)


def main() -> None:
    configure_log()
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str, help='Commands ["run", "init_db"]')
    args = parser.parse_args()
    if sys.version_info < (3, 10, 6) and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        match args.command:
            case 'init_db':
                asyncio.run(init_models())
                logger.info('Tables have been created')
            case 'run':
                asyncio.run(run())
    except SystemExit:
        exit(os.EX_OK)
    # except BaseException:
    #     logger.exception("Unexpected error occurred")
    #     exit(os.EX_SOFTWARE)


if __name__ == '__main__':
    main()
