import os

import tempfile
import win32api
import wmi
from typing import List
import subprocess


def get_params() -> dict:
    """
    Wrapper function to build a dict with all the params.

    Returns:
        dict - with all the assignment requested.
    """
    return {
        'system_familiy': get_system_family(),
        'timezone': get_timezone(),
        'UAC_enable': get_uac_state(),
        'os_vers': get_os_vers(),
        'serial_number': get_serial_number(),
        'proceesses': get_processes(),
    }


def get_system_family() -> str:
    """
    The type of the windows running on - (PC,Laptop VM...)
    Returns:
        str - with the type of the family
    """
    return wmi.WMI().Win32_ComputerSystem()[0].SystemFamily


def get_uac_state() -> bool:
    """
    Check if there is Admin that start the process.
    Returns:
        bool - if the user is admin.
    """
    uac_state = execute_to_file(
        'powershell.exe (Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows'
        '\CurrentVersion\Policies\System).EnableLUA')
    return uac_state == '1'


def get_os_vers() -> dict:
    """
    Get the os params and the build number

    Returns:
        dict - with all the params.
    """
    major, minor, build, api, extra = win32api.GetVersionEx()
    return {'major': major, 'minor': minor, 'build': build}


def get_serial_number() -> bool:
    """
    Returns:
        str - Get the machine serial number.
    """
    return wmi.WMI().Win32_PhysicalMedia()[0].SerialNumber


def execute_to_file(command):
    """
    This function execute the command
    and pass its output to a tempfile then read it back
    It is usefull for process that deploy child process
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    path = temp_file.name
    command = command + " > " + path
    proc = subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, universal_newlines=True)
    if proc.stderr:
        # if command failed return
        os.unlink(path)
        return
    with open(path, 'r') as f:
        data = f.read()
    os.unlink(path)
    return data


def get_timezone():
    """
    Get a number of the timezone

    Returns:
        int - to add or sub from utc.
    """
    return int(win32api.GetTimeZoneInformation()[0])


def get_processes() -> List[dict]:
    """
    Get all the processes that run on the local machine

    Returns:
        list(dict) - with only the relevant params
    """
    relevant_fields = []
    for process in wmi.WMI().Win32_Process():
        relevant_fields.append({
            'name': process.Name,
            'process_id': process.ProcessId,
            'thread_count': process.ThreadCount
        })
    return relevant_fields
