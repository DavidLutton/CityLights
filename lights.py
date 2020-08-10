import logging
from collections import namedtuple
from queue import Queue

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.getLogger(__name__).addHandler(logging.NullHandler())


class Communication():

    def __init__(self, ser=None):
        self.io = Queue()
        self.ser = ser

    def send(self, command):
        if self.ser is not None:
            hexdata = command.render()
            logging.debug(f'Sent {command} as {hexdata}')
            self.ser.write(bytes.fromhex(hexdata))

    def enqueue(self, command):
        self.io.put(command)
        logging.debug(f' Add {command} as {command.render()} to queue')

    def send_queue(self):
        while not self.io.empty():
            commandToSend = self.io.get()
            self.send(commandToSend)


DynaliteBytes = ['Area', 'Data1', 'OpCode', 'Data2', 'Data3', 'Join']
DynaliteBytes = DynaliteBytes[:-1]  # Drop Join

'''
Dynalite components communicate using DyNet.
The physical layer consists of a modified RS-485 TIA/EIA-485-A
serial bus running along CAT5 cable, blue and blue/white
carry the hot and cold signal respectively,
orange and orange/white carry +12 V DC,
green and green/white carry 0 V,
Brown and Brown/white are unused.
End of line termination is required [2]

DyNet 1 is the most commonly used protocol over the bus,
being messages of 8 bytes of data,
the 8th byte being a checksum.
Data is send at speed of 9600 baud, 8 bits, no parity, 1 stopbit (8N1).
Commonly there are two types of message sent via DyNet 1: logical and physical.
Logical messages talk to Areas and Channels,
and physical messages talk directly to the devices.
These 2 are typically called 1C and 5C messages,
on account of the first byte of their message.

A 1C message consist of:
[1C] [Area] [Data 1] [OpCode] [Data 2] [Data 3] [Join] [Checksum]

Area is the Logical Area the message is to control.

OpCode defines the Action to be taken on the Area.

Join is a bitswitch which can be used to filter out selected channels.

An OpCode of 00 to 03 means the action is to send the
given area into preset 1 to 4 plus 8 times the value
of Data 3 over the time specified by Data 1 and Data 2.

An OpCode of 0A to 0D means the action is to send
the given area into preset 5 to 8 plus 8 times
the value of Data 3 over the time specified by Data 1 and Data 2.

That gives a possibility of 8 × 255 presets.
A usual job uses 4 to 8,
and generally preset 4 is reserved to 'Off' or 'all to 0%'.
https://en.wikipedia.org/wiki/Dynalite 2020/07/14

'''

# https://www.dynalite.org/public-download/2947/bd40c4247432c0917b35dda8c1e3bf05


class DyNet1(namedtuple('DyNet1', DynaliteBytes)):
    # A 1C message consists of:
    # [1C] [Area] [Data 1] [OpCode] [Data 2] [Data 3] [Join] [Checksum]

    def render(self):
        hexstring = '1c' + \
            f'{self.Area:02x}' + \
            f'{self.Data1:02x}' + \
            f'{self.OpCode:02x}' + \
            f'{self.Data2:02x}' + \
            f'{self.Data3:02x}' + \
            'ff'  # Join is ignored, set to ff.

        return hexstring + DyNet1.checksum(hexstring)  # Append checksum

    @staticmethod
    def checksum(hexstring):
        # print(hexstring)
        data = bytes.fromhex(hexstring)

        checksum = abs((sum(data) & 0xFF) - 256)

        # '%2X' % (-(sum(ord(c) for c in data) % 256) & 0xFF)
        # (checksum , checksum // 256, checksum % 256)

        return f'{checksum:02x}'

    '''
    def checksum(hexstring):  # Alternative
        data = bytes.fromhex(hexstring)
        return hex(((sum(int(data.hex()[i:i+2],16) for i in range(0, len(data.hex()), 2))%0x100)^0xFF)+1)[2:]
    '''


class MockSerial():
    """Mock as a serial interface, loggs messages sent to it."""

    @staticmethod
    def write(data):
        logging.warn(f'Mock Serial Sent: {data.hex()}')
