import sys
import struct
import argparse
from file_manip_toolkit.eswap import eswap

def parse_args(args):
    parser = argparse.ArgumentParser(description='swaps bytes on a given basis')
    parser.add_argument('file', type=str,
                        help='input file')
    parser.add_argument('format', type=str,
                        help="""format to use when byte swapping.
                        possible formats are: 16 bits - h, H;
                        32 bits - l, L, i, I; 64 bits - q, Q
                        more information can be found at: 
                        https://docs.python.org/3/library/struct.html#format-characters""")
    parser.add_argument('-o', '--output', type=str,
                        help='specify where to save output, default is current working directory')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='make it wordy')

    return parser.parse_args(args)

def main():
    args = parse_args(sys.argv[1:])

    try:
        eswap.eswap_main(args.file, args.format, args.output, verbose=args.verbose)
    except(struct.error, FileNotFoundError):
        sys.exit(1)
    sys.exit(0)
