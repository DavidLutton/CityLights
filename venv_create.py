
import venv
from pathlib import Path

venvtarget = Path(f'.venv')

if not venvtarget.is_dir():
    builder = venv.EnvBuilder(
        system_site_packages=False,
        clear=False,
        symlinks=False,
        upgrade=True,
        with_pip=True
    )

    print(f'Creating new venv in: {venvtarget}')
    builder.create(venvtarget)
    print(f'New venv created in: {venvtarget}')
else:
    print(f'venv exists in: {venvtarget}')

input('Done, Press enter to close.')
