"""
Converts an MSU-1 .pcm file back into a RIFF .wav file.
"""

import argparse
import os
import sys


def generate_header(filesize):
    """
    Gets bytes representing an appropriate RIFF WAV header.

    These are common to all MSU-1 files.
    """
    return b''.join([
        b'RIFF',
        (filesize + 44).to_bytes(4, 'little'),
        b'WAVE',
        b'fmt ',
        (16).to_bytes(4, 'little'),
        (1).to_bytes(2, 'little'),
        (2).to_bytes(2, 'little'),
        (44100).to_bytes(4, 'little'),
        (176400).to_bytes(4, 'little'),
        (4).to_bytes(2, 'little'),
        (16).to_bytes(2, 'little'),
        b'data',
        filesize.to_bytes(4, 'little')])


def extract_loop_point(infile):
    """
    Grabs the loop point out of the MSU-1 file.

    Namely, the fifth through eighth bytes.
    """
    infile.seek(4)
    loop = infile.read(4)
    # What are you talking about, this is a great way to flip bytes.
    return loop[3] + loop[2] + loop[1] + loop[0]


def get_args():
    parser = argparse.ArgumentParser(
        description='Convert an MSU-1 .pcm file into a RIFF .wav file')
    parser.add_argument('infile', help='Path to the input file')
    parser.add_argument('outfile', help='Path to the output file')
    parser.add_argument(
        '-l',
        '--loop',
        help='Output the loop point to STDOUT',
        action='store_true')
    return vars(parser.parse_args())


def validate(infile):
    """
    Just ensures that the file starts with "MSU1".
    """
    infile.seek(0)
    first_four = infile.read(4).decode('utf-8')
    if first_four != 'MSU1':
        raise Exception('The input file does not appear to be an MSU-1 PCM file (read: %s)' % first_four)


def main():
    args = get_args()
    with open(args['infile'], 'rb') as infile:
        if args['loop']:
            loop = extract_loop_point(infile)
        validate(infile)
        infile_size = os.path.getsize(args['infile'])
        infile.seek(4)
        with open(args['outfile'], 'wb') as outfile:
            outfile.write(generate_header(infile_size - 4));
            outfile.write(infile.read())
    if args['loop']:
        print(str(loop))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting ...")
