import sys
import argparse

from file_manip_toolkit.unfman import CPS2Format, CustomFormat

# todo - can input a folder containing files??
# linux shells will expand '*' , windows doesn't have this - implement?

def parse_args(args):
    parser = argparse.ArgumentParser(description='(de)interleave binary files.')
    parser.add_argument('files', type=str, nargs='*',
                        help="""1 file and a number (how many files to output) to deinterleave,
                        more than 1 file to interleave
                        ex: FILE 2 will deinterleave FILE every 2 bytes into 2 files
                        ex: FILE1 FILE2 FILE3 4 will interleave the files every 4 bytes""")
    parser.add_argument('numbytes', type=str,
                        help='number of bytes to (de)interleave by')
    parser.add_argument('-o', '--output', type=str,
                        help='specify where to save output, default is current working directory')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='make it wordy')

    return parser.parse_args(args)

def main():
    args = parse_args(sys.argv[1:])

    if str(args.numbytes).lower() == 'cps2':
        formatter = CPS2Format.new(args.files, args.output, args.verbose)
    elif CustomFormat.is_number(args.numbytes):
        formatter = CustomFormat.new(args.files, args.numbytes, args.output, args.verbose)
    else:
        print('Unknown file format.', str(args.numbytes), 'Exiting')
        sys.exit(1)

    formatter.run()
    sys.exit(0)


