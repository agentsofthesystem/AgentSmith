import debugpy

from os import getenv

from application.common import logger


def init_debugger(app):
    if getenv("DEBUGGER") == "True":
        logger.info("⏳ Will Set Up Debugger!⏳ ", flush=True)

        # Set these flags forced for flask so reloader does not happen
        app.config["ENV"] = "production"
        app.config["DEBUG"] = False

        debugpy.listen(("0.0.0.0", 5678))
        logger.info(
            "⏳ VS Code debugger can now be attached, press F5 in VS Code ⏳", flush=True
        )
        debugpy.wait_for_client()
        logger.info("🎉 VS Code debugger attached, enjoy debugging 🎉", flush=True)
