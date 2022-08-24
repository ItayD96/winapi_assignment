import win32api
import wmi
import pyuac
from typing import List


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


def get_system_family():
    return wmi.WMI().Win32_ComputerSystem()[0].SystemFamily


def get_uac_state() -> bool:
    """
    Check if there is Admin that start the process.
    Returns:
        bool - if the user is admin.
    """
    return pyuac.isUserAdmin()


def get_os_vers() -> dict:
    """
    Get the os params and the build number

    Returns:
        dict - with all the params.
    """
    major, minor, build, api, extra = win32api.GetVersionEx()
    return {'major': major, 'minor': minor, 'build': build}


def get_serial_number() -> str:
    """
    Returns:
        str - Get the machine serial number.
    """
    return wmi.WMI().Win32_PhysicalMedia()[0].SerialNumber


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
