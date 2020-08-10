import sys
import subprocess
import argparse
from argparse import RawTextHelpFormatter

sys.path.append("./certifaiReferenceModelServer")


def create_parser():
    parser = argparse.ArgumentParser(description='Certifai Model Server',
                                     usage='startCertifaiModelServer [args]',
                                     formatter_class=RawTextHelpFormatter,
                                     allow_abbrev=False)
    parser.add_argument('-b', '--bind', type=str, help='The socket to bind 0.0.0.0:5111\n\n',
                        default='0.0.0.0:5111')
    parser.add_argument('-w', '--workers', type=int, help='The number of worker processes to use\n\n', default=3)
    parser.add_argument('-k', '--worker-class', type=str, help='The type of workers to use \n\n', default='gevent')
    parser.add_argument('-t', '--timeout', type=int,
                        help='Workers silent for more than this many seconds are killed and restarted.\n\n', default=30)
    parser.add_argument('--log-level', type=str, default='warn', help='log-level to use\n\n')
    return parser


def cli_parse(args):
    parser = create_parser()
    return parser.parse_args(args)


def start_all():
    args = sys.argv[1:]
    parsed_args = cli_parse(args)
    command = f"gunicorn -b {parsed_args.bind} -t {parsed_args.timeout} --workers={parsed_args.workers} " \
              f"--worker-class={parsed_args.worker_class} --log-level={parsed_args.log_level} " \
              f"certifaiReferenceModelServer.utils.local_server:app"
    subprocess.call(command.split(' '))


if __name__ == '__main__':
    start_all()
