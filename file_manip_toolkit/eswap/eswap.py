import os
import sys
import struct

def eswap_main(filepath, fmt, savepath, verbose=False):
    verboseprint = print if verbose else lambda *a, **k: None
    verboseprint('Opening file')
    fdata = open_file(filepath)

    verboseprint('Swapping endianess in file every', fmt, 'bytes')
    swapped = swap(fdata, fmt)
    filename = os.path.split(filepath)[1]
    suffix = 'swapped'

    spath = format_filename(filename, savepath, suffix)
    with open(spath, 'wb') as f:
        verboseprint('Saving', spath)
        f.write(swapped)

def swap(data, fmt):
    """Swaps byte order of given bytearray based on the format given.

    Returns a bytearray.
    """
    swap_fmt = ''.join(['>', fmt])

    try:
        swap_iter = struct.iter_unpack(fmt, data)
    except struct.error as error:
        print('ERROR:', error, 'CLOSING', file=sys.stderr)
        raise error

    try:
        swapped = [struct.pack(swap_fmt, *i) for i in swap_iter]
    except struct.error as error:
        print('ERROR:', error, '\nswap_fmt is:', swap_fmt, 'CLOSING', file=sys.stderr)
        raise error

    return b''.join(swapped)

def open_file(filepath):
    """Error handling. Returns bytearray of data in file"""
    try:
        with open(filepath, 'rb') as f:
            return bytearray(f.read())
    except FileNotFoundError as error:
        print('Error occured during opening of file:', error, file=sys.stderr)
        raise error

def format_filename(filename, savepath, suffix):
    #if no custom output, save to cwd with default name
    if not savepath:
        spath = '.'.join([filename, suffix])

    #if custom output is a folder, save default file name to that location
    elif os.path.isdir(savepath):
        tail = '.'.join([filename, suffix])
        spath = os.path.join(savepath, tail)

    #if custom output is a file, append 'swapped' to it
    else:
        spath = '.'.join([savepath, suffix])

    return spath
    