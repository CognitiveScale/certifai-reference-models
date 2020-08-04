import sys
import subprocess

sys.path.append("./certifaiReferenceModelServer")


def start_all():
    subprocess.call(
        ["gunicorn", "-b", "0.0.0.0:5111", "--workers=4", "-k=gevent", "--timeout", "20", "--capture-output",
         "--log-level",
         "debug", "certifaiReferenceModelServer.utils.local_server:app"])


if __name__ == '__main__':
    start_all()
