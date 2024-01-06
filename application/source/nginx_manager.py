import os
import platform
import requests
import sys
import subprocess
import zipfile

from jinja2 import Environment, FileSystemLoader
from threading import Thread

from application.common import logger, constants
from application.common.decorators import timeit
from application.common.exceptions import NginxException
from application.common.toolbox import _get_proc_by_name, _get_application_path

from operator_client import Operator


class NginxManager:
    def __init__(self, client: Operator) -> None:
        self._exe_name = None
        self._exe_path = None
        self._exe_full_path = None
        self._exe_thread = None

        self._client: Operator = client

        self._platform = platform.system()

    def nginx_is_found(self, exe_name: str) -> bool:
        return True if _get_proc_by_name(exe_name) else False

    def nginx_status(self, exe_name: str):
        process_info = None
        process = _get_proc_by_name(exe_name)

        if process:
            process_info = process.as_dict()
            pass

        return process_info

    def startup(self) -> None:
        self._spawn_nginx()

    def shtudown(self) -> None:
        if self._stop_nginx():
            self._exe_thread.join()

    @staticmethod
    def _print_command(list_list: list):
        output = ""
        for item in list_list:
            output += item + " "
        logger.info(output)

    def _spawn_exe(self, command: [], cwd: str) -> None:
        result = subprocess.run(
            command,
            creationflags=subprocess.DETACHED_PROCESS,  # Use this on windows-specifically.
            close_fds=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
        )

        return result

    def _launch_nginx(self, input_args={}, use_equals=False, working_dir=None) -> None:
        """
        This function is meant to launch an nginx server / reverse proxy.

        Start a generic executable server with the input arguments provided, if any.

        Args:
            input_args (dict): Dictionary of key value pairs to use
            as inputs arguments.
            use_equals (bool): If true, input arguments are appended with key=value
        """
        if not os.path.exists(self._exe_full_path):
            raise NginxException(
                f"The executable file does not exist: {self._exe_full_path}"
            )

        exe_command = [self._exe_full_path]

        format_string = '{key}="{value}"' if use_equals else "{key} {value}"

        if len(input_args.keys()) > 0:
            for arg in input_args:
                exe_command.append(format_string.format(key=arg, value=input_args[arg]))

        # Get folder
        execution_folder = os.path.dirname(self._exe_full_path)

        if working_dir:
            execution_folder = working_dir

        self._print_command(exe_command)

        self._exe_thread = Thread(
            target=lambda: self._spawn_exe(exe_command, execution_folder)
        )

        self._exe_thread.daemon = True
        self._exe_thread.start()

    def _stop_nginx(self) -> bool:
        process = None
        is_process_stopped = False

        process = _get_proc_by_name(self._exe_name)

        while process:
            process = _get_proc_by_name(self._exe_name)

            if process:
                process.terminate()
                process.wait()
                is_process_stopped = True

        return is_process_stopped

    @timeit
    def _download_nginx_server(self):
        file_name = constants.NGINX_STABLE_RELEASE_WIN.split("/")[-1]
        nginx_folder_path = os.path.join(_get_application_path(), "nginx")
        nginx_save_path = os.path.join(nginx_folder_path, file_name)

        if not os.path.exists(nginx_folder_path):
            os.makedirs(nginx_folder_path, exist_ok=True)

            response = requests.get(constants.NGINX_STABLE_RELEASE_WIN, stream=True)
            with open(nginx_save_path, "wb") as fd:
                for chunk in response.iter_content(chunk_size=128):
                    fd.write(chunk)

            with zipfile.ZipFile(nginx_save_path, "r") as zip_ref:
                zip_ref.extractall(nginx_folder_path)

    @timeit
    def _spawn_nginx(self):
        self._download_nginx_server()

        nginx_proxy_port = self._client.app.get_setting_by_name(
            constants.SETTING_NGINX_PROXY_PORT
        )

        nginx_folder = os.path.join(
            _get_application_path(), "nginx", constants.NGINX_VERSION
        )
        nginx_conf_folder = os.path.join(
            _get_application_path(), "nginx", constants.NGINX_VERSION, "conf"
        )
        nginx_conf_full_path = os.path.join(nginx_conf_folder, "nginx.conf")

        nginx_config_conf_folder = os.path.join(
            _get_application_path(), "config", "nginx"
        )
        # nginx_conf_template_full_path = os.path.join(nginx_config_conf_folder, "nginx.conf.j2")

        # Create a formatted nginx conf file.
        env = Environment(loader=FileSystemLoader(nginx_config_conf_folder))
        template = env.get_template("nginx.conf.j2")
        output_from_parsed_template = template.render(
            NGINX_PROXY_PORT=nginx_proxy_port,
        )

        if os.path.exists(nginx_conf_full_path):
            os.remove(nginx_conf_full_path)

        with open(nginx_conf_full_path, "w") as myfile:
            myfile.write(output_from_parsed_template)

        self._exe_name = "nginx.exe"
        self._exe_path = nginx_folder
        self._exe_full_path = os.path.join(self._exe_path, self._exe_name)

        # If already running, kill the nginx server.
        if self._stop_nginx():
            logger.info("NGINX: Stopped existing instance before startup...")

        try:
            self._launch_nginx(working_dir=nginx_folder)
        except Exception as error:
            message = "Unable to launch executable."
            logger.error(message)
            logger.critical(error)
            sys.exit(1)
