import abc
import time


class BaseGame:
    DEFAULT_WAIT_PERIOD = 5

    def __init__(self) -> None:
        self._game_args = []

    @abc.abstractmethod
    def startup(self) -> None:
        """Implementation Specific Startup Routine."""
        return

    @abc.abstractmethod
    def shutdown(self) -> None:
        """Implementation Specific shutdown Routine."""
        return

    def restart(self, wait_period=DEFAULT_WAIT_PERIOD) -> None:
        """Simple Routine to shutdown and re-run the startup routines."""
        self.shutdown()

        time.sleep(wait_period)

        self.startup()
