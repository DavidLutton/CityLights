#! .venv/Scripts/python.exe

import shlex
import subprocess
import sys
import time
from pathlib import Path
from pprint import pprint

sequence = [
    f'-m pip install --upgrade pip setuptools wheel',
    f'-m pip install --upgrade -r requirements.txt',
    ]

try:
    print(sys.executable)
    for line in sequence:
        print()
        print(line)
        process = subprocess.Popen([sys.executable] + shlex.split(line), stdout=subprocess.PIPE)

        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                print(output.strip().decode())
        rc = process.poll()

    # https://stackoverflow.com/a/50255019
    run = subprocess.run([sys.executable] + shlex.split('-m pip freeze'), capture_output=True)
    Path(f'./requirements_freeze.txt').write_bytes(run.stdout)

except subprocess.CalledProcessError as e:
    print(e, run)

input('Done, Press enter to close.')
