import os
import sys

_server_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _server_dir)
os.chdir(_server_dir)

from dotenv import load_dotenv

load_dotenv()

from utils.worker.email_worker import run_email_worker

if __name__ == "__main__":
    run_email_worker(poll_timeout_seconds=5)
