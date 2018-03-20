"""Finds Emerald Ash Borers from the given image, then uploads that data

To execute:

    python iotrees/eab_find.py --image examples/EAB-on-purple-trap.jpg

For local development without a dongle, send output to /dev/tty to have it
echoed to the terminal:

    python iotrees/eab_find.py --image examples/EAB-on-purple-trap.jpg --tty /dev/tty

"""

import argparse
import json

import serial

from iotrees.detect import detect


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=True, help='Path to image containing EABs.')
    ap.add_argument('-t', '--tty', default='/dev/ttyUSB0', help='Which TTY device to send results to.')
    args = ap.parse_args()

    bug_count = detect(args.image)
    latitude = '100'
    longitude = '100'
    coverage = '55'

    # Dummy data to send with the bug_count
    outgoing = {
        "lat": latitude,
        "lon": longitude,
        "count": bug_count,
        "coverage": coverage,
    }

    # Set serial for digi dongle and send the data to digi
    # Must send as bytestring
    s = serial.Serial(args.tty, 9600, timeout=1)
    s.write(json.dumps(outgoing).encode('utf-8'))


if __name__ == '__main__':
    main()
