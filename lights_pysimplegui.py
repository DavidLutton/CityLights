
import os
from pprint import pprint
from time import sleep

import PySimpleGUI as sg
import serial
from serial.tools.list_ports import comports

from lights import Communication, DyNet1, MockSerial

rpi = False

if 'raspberrypi' in os.uname():
    rpi = True
    from rpi_backlight import Backlight

    backlight = Backlight()
    print(backlight.brightness)
    with backlight.fade(duration=2):
        backlight.brightness = 26
    
for port in comports():
    # print(dir(port))
    # print(port.device)
    ser = serial.Serial(port.device, 9600, timeout=10)  # open serial port
    print(ser.name)         # check which port was really used
    lights = Communication(ser)
    break
else:
    lights = Communication(MockSerial)

# a = DyNet1(0, 254, 3, 2, 1)
# a, a.render()

# lights.enqueue(DyNet1(0,1,2,3,4))

# lights.send_queue()

# f'{255:02x}', int('ff', 16)


grids = (13, 4)
tab_common_layout = [
    [
        sg.Button('Wall On', size=grids),
        sg.Button('Wall Off', size=grids),
        sg.Button('Full Brightness', size=grids),
    ],
    [
        sg.Button('Set b 1', size=grids),
        sg.Button('Set b 2', size=grids),
        sg.Button('Set b 3', size=grids),
    ],
    [
        sg.Button('Set c 1', size=grids),
        sg.Button('Set c 2', size=grids),
        sg.Button('Set c 3', size=grids),
    ],
]
gridsfourbytwo = (12, 7)
tab_stage_layout = [
    [
        sg.Button('Setup A', size=gridsfourbytwo),
        sg.Button('Setup B', size=gridsfourbytwo),
        sg.Button('Setup C', size=gridsfourbytwo),
        sg.Button('Setup D', size=gridsfourbytwo),
    ],
    [
        sg.Button('Setup E', size=gridsfourbytwo),
        sg.Button('Setup F', size=gridsfourbytwo),
        sg.Button('Setup G', size=gridsfourbytwo),
        sg.Button('All Off', size=gridsfourbytwo, button_color='black on red'),
    ],
]

gridseightbytwo = (4, 4)
tab_adjust_layout = [
    [
        sg.Button('↑ 1', size=gridseightbytwo),
        sg.Button('↑ 2', size=gridseightbytwo),
        sg.Button('↑ 3', size=gridseightbytwo),
        sg.Button('↑ 4', size=gridseightbytwo),
        sg.Button('↑ 5', size=gridseightbytwo),
        sg.Button('↑ 6', size=gridseightbytwo),
        sg.Button('↑ 7', size=gridseightbytwo),
        sg.Button('↑ 8', size=gridseightbytwo),
    ],
    [
        sg.Button('↓ 1', size=gridseightbytwo),
        sg.Button('↓ 2', size=gridseightbytwo),
        sg.Button('↓ 3', size=gridseightbytwo),
        sg.Button('↓ 4', size=gridseightbytwo),
        sg.Button('↓ 5', size=gridseightbytwo),
        sg.Button('↓ 6', size=gridseightbytwo),
        sg.Button('↓ 7', size=gridseightbytwo),
        sg.Button('↓ 8', size=gridseightbytwo),
    ],
]

col_manual_labels = [
    [sg.Text('Area', pad=((0, 0), (25, 20)))],
    [sg.Text('Data 1', pad=((0, 0), (0, 20)))],
    [sg.Text('OpCode', pad=((0, 0), (0, 20)))],
    [sg.Text('Data 2', pad=((0, 0), (0, 20)))],
    [sg.Text('Data 3', pad=((0, 0), (0, 20)))],
]

col_manual_sliders = [
    [sg.Slider((0, 16), 0, 1, orientation="h", size=(40, 15), key="-Manual Area-", enable_events=True)],
    [sg.Slider((0, 255), 128, 1, orientation="h", size=(40, 15), key="-Manual Data 1-", enable_events=True)],
    [sg.Slider((0, 255), 128, 1, orientation="h", size=(40, 15), key="-Manual OpCode-", enable_events=True)],
    [sg.Slider((0, 255), 128, 1, orientation="h", size=(40, 15), key="-Manual Data 2-", enable_events=True)],
    [sg.Slider((0, 255), 128, 1, orientation="h", size=(40, 15), key="-Manual Data 3-", enable_events=True)],
]

tab_manual_control_layout = [
    [sg.Column(col_manual_labels), sg.Column(col_manual_sliders)],

    [sg.Text('', size=(58, 1), key='render repr', font=('Helvetica', 14, 'bold'))],
    [sg.Text('', size=(16, 1), key='render hex', font=('Helvetica', 14, 'bold'))],
    [sg.Button('Send'), sg.Button('Send All')],
    ]

tab_backlight_control_layout = [
    [sg.Text('Backlight')],
    [sg.Slider((6, 100), 26, 2, orientation="h", size=(40, 15), key="Backlight", enable_events=True)],
]

tab_exit_layout = [[sg.Text("Exit from City Lights UI")], [sg.Button("Exit", key='--Exit--')]]

padding = ' ' * 2
layout = [[
    sg.TabGroup([[
        sg.Tab(padding + 'Presets' + padding, tab_stage_layout),
        sg.Tab(padding + 'Adjust' + padding, tab_adjust_layout, visible=True),
        sg.Tab(padding + 'Common' + padding, tab_common_layout, visible=False),
        sg.Tab(padding + 'Manual' + padding, tab_manual_control_layout, visible=True),
        sg.Tab(padding + 'Backlight' + padding, tab_backlight_control_layout, visible=True),
        sg.Tab(padding + 'Exit' + padding, tab_exit_layout, visible=True),
    ]], border_width=0)
]]

# sg.SetOptions(element_padding=(40,20))
# sg.SetOptions()

window = sg.Window(
    'Lights',  # Title
    layout,
    no_titlebar = True if rpi else False,
    location = (0, 0) if rpi else (50, 50),
    size=(800, 480),
    keep_on_top=False,
    # auto_size_buttons=True,
    # auto_size_text=True,
    font=('Helvetica', 18 if rpi else 14, 'bold'),
    # default_element_size=(30, 1)
)
lastsetup = None
# Create an event loop
while True:
    event, values = window.read(timeout=10000)  # set time out
    # count consecutive no UI event periods, raise a lock screen

    if event == "--Exit--" or event == sg.WIN_CLOSED:
        break

    area = int(values['-Manual Area-'])
    data1 = int(values['-Manual Data 1-'])
    opcode = int(values['-Manual OpCode-'])
    data2 = int(values['-Manual Data 2-'])
    data3 = int(values['-Manual Data 3-'])

    dynet = DyNet1(area, data1, opcode, data2, data3)

    if event.startswith('-Manual'):
        window['render hex'].Update(dynet.render())
        window['render repr'].Update(dynet)

    if event == 'Send':
        lights.send(dynet)

    if event == 'Send All':
        for area in [1, 2, 3, 4, 5, 6, 7, 8]:
            lights.send(DyNet1(area, data1, opcode, data2, data3))

    if event == 'Wall On':
        for area in [1, 2, 3, 4, 5, 6, 7, 8]:
            lights.enqueue(DyNet1(area, 255, 0, 0, 1))
        lights.send_queue()

    if event == 'Wall Off':
        for area in [1, 2, 3, 4, 5, 6, 7, 8]:
            lights.enqueue(DyNet1(area, 255, 3, 0, 0))
        lights.send_queue()

    if event == 'Full Brightness':
        for area in [1, 2, 3, 4, 5, 6, 7, 8]:
            lights.enqueue(DyNet1(area, 255, 0, 0, 2))
        lights.send_queue()

    rate = 64
    if event == 'Setup A':
        lights.send(DyNet1(0, rate, 0, 0, 0))

    if event == 'Setup B':
        lights.send(DyNet1(0, rate, 1, 0, 0))

    if event == 'Setup C':
        lights.send(DyNet1(0, rate, 2, 0, 0))

    if event == 'Setup D':
        lights.send(DyNet1(0, rate, 10, 0, 0))

    if event == 'Setup E':
        lights.send(DyNet1(0, rate, 11, 0, 0))

    if event == 'Setup F':
        lights.send(DyNet1(0, rate, 12, 0, 0))

    if event == 'Setup G':
        lights.send(DyNet1(0, rate, 13, 0, 0))

    if event == 'All Off':
        lights.send(DyNet1(0, 255, 13, 0, 0))

    if event.startswith('↓') or event.startswith('↑'):
        # Adjust an area 1 count ↑ or ↓
        part = event.split(' ')
        heading, area = part[0], int(part[1])

        if heading == '↑':
            lights.send(DyNet1(area, 20, 6, 0, 0))

        if heading == '↓':
            lights.send(DyNet1(area, 20, 5, 0, 0))

    if event == 'Backlight':
        if 'raspberrypi' in os.uname():
            backlight.brightness = int(values['Backlight'])

    print(f'Event: {event}')
    if event.startswith('Setup'):
        lastsetup = event.split(' ')[1]
    print(f'Last Setup: {lastsetup}')
window.close()
