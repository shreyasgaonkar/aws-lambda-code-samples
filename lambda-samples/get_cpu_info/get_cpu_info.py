import os
import subprocess
import json
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Lambda's default working directory:")
    logger.info(os.environ["LAMBDA_TASK_ROOT"])

    print_tmp_directory_info()
    print_filesystem_info()
    print_system_info()

    return {"statusCode": 200, "body": json.dumps("Completed execution.")}


def print_tmp_directory_info():
    try:
        os.chdir("/tmp")
        tmp_contents = os.listdir("/tmp")
        logger.info(f"/tmp contents: {tmp_contents}")
    except Exception as e:
        logger.error(f"Error accessing /tmp directory: {e}")


def round_numerical(value, precision=2):
    return round(value, precision)


def print_filesystem_info():
    try:
        statvfs = os.statvfs(".")
        # Size of filesystem in MegaBytes
        size_mb = round_numerical(statvfs.f_frsize * statvfs.f_blocks / (1024 * 1024))
        # Actual number of free MegaBytes
        free_mb = round_numerical(statvfs.f_frsize * statvfs.f_bfree / (1024 * 1024))
        # Number of free MegaBytes
        avail_mb = round_numerical(statvfs.f_frsize * statvfs.f_bavail / (1024 * 1024))

        logger.info(f"Size of filesystem in MegaBytes: {size_mb}")
        logger.info(f"Actual number of free MegaBytes: {free_mb}")
        logger.info(f"Number of free MegaBytes: {avail_mb}")
    except Exception as e:
        logger.error(f"Error fetching filesystem info: {e}")


def run_command(command):
    """Run command securely"""
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            error_message = f"Command '{' '.join(command)}' failed with return code {process.returncode}."
            logger.error(error_message)
            logger.error(f"stderr: {stderr.decode('utf-8').strip()}")
            raise RuntimeError(error_message)

        return stdout.decode("utf-8")

    except Exception as e:
        logger.error(f"Error executing command '{' '.join(command)}': {e}")
        raise e


def print_system_info():
    try:
        logger.info("cat /etc/os-release:")
        os_release_info = run_command(["cat", "/etc/os-release"])
        logger.info(os_release_info)

        logger.info("uname -a:")
        uname_info = run_command(["uname", "-a"])
        logger.info(uname_info)

        logger.info("cat /proc/cpuinfo:")
        cpu_info = run_command(["cat", "/proc/cpuinfo"])
        logger.info(cpu_info)

        logger.info("")
    except Exception as e:
        logger.error(f"Error fetching system info: {e}")
