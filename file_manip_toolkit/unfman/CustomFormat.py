import os
import sys
from struct import Struct, error
from file_manip_toolkit.helpers import is_number
from file_manip_toolkit.unfman.FileFormat import FileFormat

class CustomFormat(FileFormat):
    def run(self):
        if is_number(self._filepaths[1]):
            self._nsplit = int(self._filepaths[1])

        if self._nsplit:
            final = self.deinterleave_file()

        elif len(self._filepaths) >= 2:
            final = self.interleave_files()

        else:
            print('Something broke - number of filepaths:', len(self._filepaths))
            raise Exception

        savepaths = self.format_savepaths()
        self.save(savepaths, final)

    def interleave_files(self):
        self.verboseprint('Opening files')
        data = [self.open_file(fp) for fp in self._filepaths]

        self.verboseprint('Interleaving files every', self._numbytes, 'bytes')

        return [interleave(data, int(self._numbytes))]

    def deinterleave_file(self):
        self.verboseprint('Opening file')
        data = self.open_file(self._filepaths[0])

        self.verboseprint('Deinterleaving file every', self._numbytes, 'bytes')
        self.verboseprint('Producing', self._nsplit, 'files')

        return deinterleave(data, int(self._numbytes), self._nsplit)

    def _filenames_and_suffixes(self):
        if self._nsplit:
            filenames = [os.path.split(self._filepaths[0])[1]] * self._nsplit
            suffixes = [str(i) for i in range(self._nsplit)]

        # elif len(self._filepaths) > 2:
        #     filenames = ['.'.join([os.path.split(fname)[1] for fname in self._filepaths])]
        #     suffixes = ['combined']

        else:
            filenames = ['.'.join([os.path.split(fname)[1] for fname in self._filepaths])]
            suffixes = ['combined']

        return filenames, suffixes

    def format_savepaths(self):
        filenames, suffixes = self._filenames_and_suffixes()
        #if no custom output, save to cwd with default name
        if not self._savepaths:
            fnames = [os.path.split(fname)[1] for fname in filenames]
            spaths = ['.'.join([fname, s]) for fname, s in zip(fnames, suffixes)]

        #if custom output is a folder, save default file name to that location
        elif os.path.isdir(self._savepaths):
            head = self._savepaths
            tails = ['.'.join([fname, s]) for fname, s in zip(filenames, suffixes)]
            spaths = [os.path.join(head, tail) for tail in tails]

        #if custom output is a file, append number to the end of it
        else:
            spaths = ['.'.join([self._savepaths, s]) for s in suffixes]

        return spaths

# Factory method
def new(filepaths, numbytes, savepaths, verbose):
    return CustomFormat(filepaths, numbytes, savepaths, verbose)

def deinterleave(data, nbytes, nsplit):
    """Deinterleaves one bytearray into nsplit many bytearrays on a nbytes basis.

    Returns a list of bytearrays.
    """
    deinterleaved = [[] for n in range(nsplit)]

    deinterleave_s = Struct('c' * nbytes)

    try:
        deinterleave_iter = deinterleave_s.iter_unpack(data)
    except error as err:
        #this error can be many things, handling generically until otherwise
        print('ERROR:', err, 'CLOSING', file=sys.stderr)
        raise err

    #this could cause rounding errors?
    iterlen = int(len(data) / (nbytes * nsplit))
    for _ in range(iterlen):
        for i, _ in enumerate(deinterleaved):
            try:
                next_ = next(deinterleave_iter)
            except StopIteration:
                pass
            deinterleaved[i].extend([*next_])

    return [b''.join(delist) for delist in deinterleaved]

def interleave(data, nbytes):
    """Interleaves a list of bytearrays together on a nbytes basis.

    Returns a bytearray.
    """
    interleave_s = Struct('c' * nbytes)
    iters = []

    for inter in data:
        try:
            iters.append(interleave_s.iter_unpack(inter))
        except error as err:
            print('ERROR:', err, 'CLOSING', file=sys.stderr)
            raise err

    interleaved = []
    #this could cause rounding errors?
    iterlen = int(len(data[0]) / nbytes)
    for _ in range(iterlen):
        nexts = [next(iter_) for iter_ in iters]
        interleaved.extend([b''.join(val) for val in nexts])

    return b''.join(interleaved)
