import os
import platform
import subprocess

from application.common import logger
from application.common.toolbox import _get_proc_by_name
from application.common.exceptions import GenericExeException


class GenericExecutableManager:
    def __init__(self, exe_name: str, exe_path: str) -> None:
        self._exe_name = exe_name
        self._exe_path = exe_path
        self._exe_full_path = self._exe_path + os.sep + self._exe_name

        self._exe_full_path = os.path.join(self._exe_path, self._exe_name)

        self._platform = platform.system()

    @staticmethod
    def _print_command(list_list: list):
        output = ""
        for item in list_list:
            output += item + " "
        logger.info(output)

    def executable_is_found(self, exe_name: str) -> bool:
        return True if _get_proc_by_name(exe_name) else False

    def executable_status(self, exe_name: str):
        process_info = None
        process = _get_proc_by_name(exe_name)

        if process:
            process_info = process.as_dict()
            pass

        return process_info

    def launch_executable(self, input_args={}, use_equals=False) -> None:
        """
        This fucntion is meant to launch any basic executable.

        Start a generic executable server with the input arguments provided, if any.

        Args:
            input_args (dict): Dictionary of key value pairs to use
            as inputs arguments.
            use_equals (bool): If true, input arguments are appended with key=value
        """
        if not os.path.exists(self._exe_full_path):
            raise GenericExeException(
                f"The executable file does not exist: {self._exe_full_path}"
            )

        exe_command = [self._exe_full_path]

        # TODO - Put a check that the exe is not already running!
        format_string = '{key}="{value}"' if use_equals else '{key} "{value}"'

        if len(input_args.keys()) > 0:
            for arg in input_args:
                exe_command.append(format_string.format(key=arg, value=input_args[arg]))

        # Get folder
        parent_folder = os.path.dirname(self._exe_full_path)

        if self._platform == "Windows":
            self._print_command(exe_command)
            return subprocess.Popen(
                exe_command,
                creationflags=subprocess.DETACHED_PROCESS,  # Use this on windows-specifically.
                close_fds=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=parent_folder,
            )
        else:  # Linux
            exe_command.append("&")
            self._print_command(exe_command)
            return subprocess.Popen(
                exe_command,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                cwd=parent_folder,
            )

    def kill_executable(self, exe_name: str) -> bool:
        is_process_stopped = False

        process = _get_proc_by_name(exe_name)

        if process:
            # is_process_stopped = True
            process.terminate()
            process.wait()
            is_process_stopped = True

        else:
            # process is None b/c it's not there... true in this case.
            is_process_stopped = True

        return is_process_stopped
