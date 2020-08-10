# CityLights
Lighting controller for a Dynalite DyNet1 system  

Currently this attaches to the first found serial interface  
if none a MockSerial interface is created and this prints what is sent to it.


## On Windows
### Install
Get Python from [Python.org](https://www.python.org/downloads/)  

Install Python and tick "Add Python to PATH" in the installer.  

Run `venv_create` which originates from [DavidLutton / Create venv and config for Python & VS Code](https://gist.github.com/DavidLutton/ca1aed5292faba67cfdf2a6fc879fab2)  

Then `venv_install` to install modules

### Run
Then `lights_pysimplegui_windows_run`


## On Linux
### Install
Run `python3 venv_create.py` which originates from [DavidLutton / Create venv and config for Python & VS Code](https://gist.github.com/DavidLutton/ca1aed5292faba67cfdf2a6fc879fab2)  

Then `./.venv/bin/python3 venv_install.py` to install modules

### Run
Then `./.venv/bin/python3 lights_pysimplegui.py`

# References
[Dynalite Technical Overview](https://www.dynalite.org/public-download/2947/bd40c4247432c0917b35dda8c1e3bf05)  
[Dynalite - Wikipedia](https://en.wikipedia.org/wiki/Dynalite)
