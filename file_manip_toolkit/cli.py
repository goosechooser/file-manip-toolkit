import argparse
import sys
from file_manip_toolkit.CPS2Format import CPS2Format
from file_manip_toolkit.CustomFormat import CustomFormat

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def eswap_main():
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
    args = parser.parse_args()

    formatter = CustomFormat([args.file], None, args.output, verbose=args.verbose)
    formatter.eswap_file(args.format)

def unfman_main():
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
    # parser.add_argument('-f', '--format', type=str,
    #                     help='specify a file format, options are: \'cps2\' or \'neogeo\'')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='make it wordy')

    args = parser.parse_args()
    # print(args)
    #print(len(args.files))

    #Do special things wrt how saved files are named for neogeo and cps2
    if is_number(args.numbytes):
        # print('No format selected')
        formatter = CustomFormat(args.files, args.numbytes, args.output, verbose=args.verbose)
    elif str(args.numbytes).lower() == 'cps2':
        # print('CPS2 format selected')
        formatter = CPS2Format(args.files, None, args.output, verbose=args.verbose)
        #This is kludgey and I hate it
        # args.files.append(0)
    else:
        print('Unknown file format.', str(args.numbytes), 'Exiting')
        sys.exit(1)

    formatter.run()
