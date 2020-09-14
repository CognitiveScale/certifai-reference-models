""" 
Copyright (c) 2020. Cognitive Scale Inc. All rights reserved.
Licensed under CognitiveScale Example Code License https://github.com/CognitiveScale/certifai-reference-models/blob/450bbe33bcf2f9ffb7402a561227963be44cc645/LICENSE.md
"""
import platform
import sys
import subprocess
import argparse
from argparse import RawTextHelpFormatter
import socket

sys.path.append("./certifaiReferenceModelServer")

_supported_worker_class = [
    'sync',
    'gevent',
    'gthread'
]
_supported_log_levels = [
    'debug',
    'info',
    'warning',
    'error',
    'critical'
]


def create_parser():
    parser = argparse.ArgumentParser(description='Certifai Model Server',
                                     usage='startCertifaiModelServer [args]',
                                     formatter_class=RawTextHelpFormatter,
                                     allow_abbrev=False)
    parser.add_argument('-b', '--bind', type=str, help='The socket to bind 0.0.0.0:5111\n\n',
                        default='0.0.0.0:5111')
    parser.add_argument('-w', '--workers', type=int, help='The number of worker processes to use\n\n', default=3)
    parser.add_argument('-k', '--worker-class', type=str,
                        help=f'The type of workers to use. supported worker class {_supported_worker_class} \n\n',
                        default='gevent')
    parser.add_argument('-t', '--timeout', type=int,
                        help='Workers silent for more than this many seconds are killed and restarted.\n\n', default=30)
    parser.add_argument('--log-level', type=str, default='warning',
                        help=f'log-level to use supported log-level {_supported_log_levels}\n\n')
    return parser


def _validate_user_input(parsed_args):
    # validate host:port for bind
    try:
        bind_ip, bind_port = parsed_args.bind.split(':')
    except ValueError as e:
        raise ValueError(f'incorrect argument to bind. must be of format <ip/hostname>:<port> \n error {e}') from None

    try:
        if not ((socket.gethostbyname(bind_ip) == bind_ip) or (socket.gethostbyname(bind_ip) != bind_ip)):
            raise ValueError('cannot parse ip address/hostname. Incorrect argument to bind')
    except (socket.gaierror, UnicodeError):
        raise ValueError('not a valid ip address/hostname') from None

    # validate worker_class
    if parsed_args.worker_class not in _supported_worker_class:
        raise ValueError(f"invalid argument for worker_class. only {_supported_worker_class} is supported")

    # validate log-level
    if parsed_args.log_level not in _supported_log_levels:
        raise ValueError(f"invalid argument for log-level.only {_supported_log_levels} is supported ")

    return parsed_args


def cli_parse(args):
    parser = create_parser()
    return parser.parse_args(args)


def start_all():
    args = sys.argv[1:]
    parsed_args = cli_parse(args)
    # for veracode static scan
    parsed_args = _validate_user_input(parsed_args)
    if platform.system() != 'Windows':
        command = f"gunicorn -b {parsed_args.bind} -t {parsed_args.timeout} --workers={parsed_args.workers} " \
                  f"--worker-class={parsed_args.worker_class} --log-level={parsed_args.log_level} " \
                  f"certifaiReferenceModelServer.utils.local_server:app"
        subprocess.call(command.split(' '))
    else:
        from certifaiReferenceModelServer.utils.local_server import start_flask_native
        start_flask_native(parsed_args.bind)


if __name__ == '__main__':
    start_all()
