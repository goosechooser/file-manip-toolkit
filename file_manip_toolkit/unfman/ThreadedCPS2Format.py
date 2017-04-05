import os
import time
from struct import Struct
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

from file_manip_toolkit.unfman.CustomFormat import CustomFormat

# Current times for deinterleave/interleave are ~10s each
# Implement threading for a speedup?

class ThreadedCPS2Format(CustomFormat):
    def __init__(self, filepaths, numbytes, savepaths, verbose):
        super(ThreadedCPS2Format, self).__init__(filepaths, numbytes, savepaths, verbose)
        self._pool = ThreadPool(2)

    def run(self):
        if len(self._filepaths) == 1:
            final = self.deinterleave_file()
        else:
            final = self.interleave_files()

        savepaths = self.format_savepaths()
        self.save(savepaths, final)

    def interleave_files(self):
        """Interleaves a set of 4 cps2 graphics files."""

        self.verboseprint('Opening files')
        data = [self.open_file(fp) for fp in self._filepaths]

        self.verboseprint('Splitting files')
        args = zip(data, [2] * len(data))
        split_data = self._pool.starmap(deinterleave, args)

        # initial split gives us something like:
        # [['13e', '13o'], ['15e', '15o'], ['17e', '17o'], ['19e', '19o']]

        self.verboseprint('First pass - interleaving every 2 bytes')
        flat = [e for tupl in split_data for e in tupl]
        args = zip(flat[0::1], flat[4::1], [2] * len(flat[:4]))
        results = self._pool.starmap(interleave, args)

        # first interleave will produce:
        # ['13e.15e', '13o.15o', '17e.19e', '17o.19o']

        # rearrage it to be:
        # ['13e.15e', '17e.19e', '13o.15o', '17o.19o']

        self.verboseprint('Second pass - interleaving every 64 bytes')
        args = zip(results[0::2], results[1::2])
        second_interleave = zip(*args, [64] * len(results))

        results = self._pool.starmap(interleave, second_interleave)

        self.verboseprint('Last pass - interleaving every 1048576 bytes')
        final = [interleave(*results, 1048576)]

        return final

    def deinterleave_file(self):
        """Deinterleaves a interleaved cps2 graphics file."""

        self.verboseprint('Opening files')
        data = self.open_file(self._filepaths[0])

        # produces 1 tuple
        self.verboseprint('First pass - deinterleaving every 1048576 bytes')
        first = deinterleave(data, 1048576)
        # first = deinterleave(data, 1048576, self._pool)
        # return first

        self.verboseprint('Second pass - deinterleaving every 64 bytes')
        args = [(half, 64) for half in first]
        second = self._pool.starmap(deinterleave, args)
        #produces 2 tuples

        self.verboseprint('Final pass - deinterleaving every 2 bytes')
        args = []
        for reshaped in [zip(quarter, [2] *len(quarter)) for quarter in second]:
            args.extend([*reshaped])

        final = self._pool.starmap(deinterleave, args)
        #produces 4 tuples - want to flatten them

        flat = [e for tupl in final for e in tupl]
        args = zip(flat[0::1], flat[4::1], [2] * len(flat[:4]))

        results = self._pool.starmap(interleave, args)

        return results

    def _filenames_and_suffixes(self):
        if len(self._filepaths) == 1:
            # print("deinterleave")
            filepaths = [os.path.split(fpath)[1] for fpath in self._filepaths]
            splits = filepaths[0].split('.')
            suffixes = splits[1:-1]
            filenames = [splits[0]] * 4

        else:
            # print("interleave")
            filepaths = [os.path.split(fpath)[1] for fpath in self._filepaths]
            splits = [name.split('.') for name in filepaths]
            bases = [base[0] for base in splits]
            nums = [str(num[1]) for num in splits]
            filenames = ['.'.join([bases[0], *nums])]
            suffixes = ['combined']

        return filenames, suffixes

# factory
def new(filepaths, savepaths, verbose):
    return ThreadedCPS2Format(filepaths, None, savepaths, verbose)

def threaded_deinterleave(args):
    """Deinterleaves a bytearray.

    Returns two bytearrays.
    """
    print(len(args))
    data, struct_ = args

    evens = []
    odds = []
    deinterleave_iter = struct_.iter_unpack(data)

    for i in deinterleave_iter:
        evens.extend([*i])
        odds.extend([*next(deinterleave_iter)])

    return b''.join(evens), b''.join(odds)

# def deinterleave(data, num_bytes, pool):

#     deinterleave_s = Struct('c' * num_bytes)

#     results = pool.map(threaded_deinterleave, (data, deinterleave_s))
#     # will return list of tuples
#     # need to turn those tuples in something else
#     evens = results[0::1]
#     odds = results[1::1]

#     return b''.join(evens), b''.join(odds)

def deinterleave(data, num_bytes):
    """Deinterleaves a bytearray.

    Returns two bytearrays.
    """
    # data, num_bytes = args

    evens = []
    odds = []
    deinterleave_s = Struct('c' * num_bytes)
    deinterleave_iter = deinterleave_s.iter_unpack(data)

    for i in deinterleave_iter:
        evens.extend([*i])
        odds.extend([*next(deinterleave_iter)])

    return b''.join(evens), b''.join(odds)

def interleave(file1, file2, num_bytes):
    """Interleaves two bytearray buffers together.

    Returns a bytearray.
    """
    # file1, file2, num_bytes = args

    interleaved = []
    interleave_s = Struct('c' * num_bytes)
    file1_iter = interleave_s.iter_unpack(file1)
    file2_iter = interleave_s.iter_unpack(file2)

    for i in file1_iter:
        file2_next = next(file2_iter)
        interleave_temp = [*i, *file2_next]
        interleaved.extend(interleave_temp)

    return  b''.join(interleaved)

def dummy(args):
    return args

if __name__ == '__main__':
    TESTDIR = 'tests\\testdir'
    INTERLEAVE_FILES = ['cps2_test.13', 'cps2_test.15', 'cps2_test.17', 'cps2_test.19']
    DEINTERLEAVE_FILES = ['cps2_test.13.15.17.19.combined']
    files = ['\\'.join([TESTDIR, name]) for name in DEINTERLEAVE_FILES]

    formatter = new(files, '', False)
    a = time.perf_counter()
    formatter.deinterleave_file()
    b = time.perf_counter()
    print(b - a)

    files = ['\\'.join([TESTDIR, name]) for name in INTERLEAVE_FILES]
    formatter = new(files, '', False)
    a = time.perf_counter()
    formatter.interleave_files()
    b = time.perf_counter()
    print(b - a)

