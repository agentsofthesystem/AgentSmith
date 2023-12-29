import platform
import psutil

from application.common.toolbox import get_size


def get_platform_info():
    system = platform.uname()

    cpufreq = psutil.cpu_freq()
    svmem = psutil.virtual_memory()

    return {
        "platform": {
            "system": system.system,
            "node_name": system.node,
            "release": system.release,
            "version": system.version,
            "machine": system.machine,
            "processor": system.processor,
        },
        "cpu": {
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "max_frequency": f"{cpufreq.max:.2f}Mhz",
            "min_frequency": f"{cpufreq.min:.2f}Mhz",
            "current_frequency": f"{cpufreq.current:.2f}Mhz",
        },
        "memory": {
            "total": get_size(svmem.total),
            "available": get_size(svmem.available),
            "used": get_size(svmem.used),
            "percentage": f"{svmem.percent}%",
        },
    }
