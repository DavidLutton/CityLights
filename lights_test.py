from lights import DyNet1

tests = [
    '1c0a64000002ff75',
    '1c01ff030000ffe2',
    '1c02ff030000ffe1',
    '1c03ff030000ffe0',
    '1c04ff030000ffdf',
    '1c05ff030000ffde',
    '1c06ff030000ffdd',
    '1c07ff030000ffdc',
    '1c08ff030000ffdb'
    '1c0a64010001ff75',
    '1c01ff000001ffe4',
    '1c02ff000001ffe3',
    '1c03ff000001ffe2',
    '1c04ff000001ffe1',
    '1c05ff000001ffe0',
    '1c06ff000001ffdf',
    '1c07ff000001ffde',
    '1c08ff000001ffdd',
    '1C03FF010000FFE2',
    '1C03FF010000FFE2',
    '1C03FF010001FFE1',
    '1C03FF020000FFE1',

    '1C0309030000FFD6',
    '1C0309010000FFD8',
    '1C03090A0000FFCF',
    '1C03090A0001FFCE',
    '1C03090b0000FFCE',
    '1C03090b0001FFCD',
    '1C03090C0000FFCD',
    '1C03090C0001FFCC',
    '1C03090D0000FFCC',
    '1C03090D0001FFCB',
    '1C03090D0001FFCB',
]
for test in tests:
    hexstring = test[0:-2]
    testchecksum = test[-2:].lower()
    print(hexstring, testchecksum)

    print(DyNet1.checksum(hexstring), testchecksum, DyNet1.checksum(hexstring) == testchecksum)
