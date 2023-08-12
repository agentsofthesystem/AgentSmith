import os
import psutil


@staticmethod
def recursive_chmod(parent_path: str) -> None:
    for root, dirs, files in os.walk(parent_path):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o777)
        for f in files:
            os.chmod(os.path.join(root, f), 0o777)


@staticmethod
def _get_proc_by_name(process_name: str):
    process = None

    current_procs = list((p for p in psutil.process_iter()))

    for proc in current_procs:
        proc_name = proc.name()

        if proc_name == "" or proc_name == " ":
            continue

        if proc_name == process_name:
            process = proc
            break

    return process
