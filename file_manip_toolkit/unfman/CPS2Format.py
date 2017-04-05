"""
License info here?
"""
import os
from struct import Struct
from file_manip_toolkit.unfman.CustomFormat import CustomFormat

# Current times for deinterleave/interleave are ~10s each
# Implement threading for a speedup?

class CPS2Format(CustomFormat):
    """This class handles the deinterleaving and interleaving of CPS2 files.

    Its deinterleave() and interleave() are 'optimized' based on knowing exactly
    how many files are expected, and the size of the files.
    """
    def run(self):
        """
        Deinterleaves/Interleaves the group of files. Saves them.
        The factory function should be used to set everything up,\\
        and then this can be called.
        """
        if len(self._filepaths) == 1:
            final = self.deinterleave_file()
        else:
            final = self.interleave_files()

        savepaths = self.format_savepaths()
        self.save(savepaths, final)

    def interleave_files(self):
        """
        Interleaves a group of 4 CPS2 graphics files.

        Returns:
            a :obj:`list` containing a single :obj:`bytes`.\\
            This is the final interleaved file. This can then be\\
            saved to a file.
        """

        self.verboseprint('Opening files')
        data = [self.open_file(fp) for fp in self._filepaths]

        self.verboseprint('Splitting files')
        split_data = [deinterleave(fsplit, 2) for fsplit in data]

        self.verboseprint('First pass - interleaving every 2 bytes')
        interleaved = []
        data_iter = iter(split_data)

        for sdata in data_iter:
            next_data = next(data_iter)
            even = interleave(sdata[0], next_data[0], 2)
            odd = interleave(sdata[1], next_data[1], 2)
            interleaved.append((even, odd))

        self.verboseprint('Second pass - interleaving every 64 bytes')
        inter_iter = iter(interleaved)

        second_interleave = []
        for i in inter_iter:
            next_data = next(inter_iter)
            second_interleave.append(interleave(i[0], next_data[0], 64))
            second_interleave.append(interleave(i[1], next_data[1], 64))

        self.verboseprint('Last pass - interleaving every 1048576 bytes')
        final = [interleave(second_interleave[0], second_interleave[1], 1048576)]

        return final

    def deinterleave_file(self):
        """
        Deinterleaves a single interleaved CPS2 graphics file.

        Returns:
            a :obj:`list` of :obj:`bytes`. These can then be saved to files.
        """

        self.verboseprint('Opening files')
        data = self.open_file(self._filepaths[0])

        self.verboseprint('First pass - deinterleaving every 1048576 bytes')
        first = deinterleave(data, 1048576)

        second = []
        self.verboseprint('Second pass - deinterleaving every 64 bytes')
        for half in first:
            second.extend(deinterleave(half, 64))

        final = []
        self.verboseprint('Final pass - deinterleaving every 2 bytes')
        for quarter in second:
            final.extend(deinterleave(quarter, 2))

        deinterleaved = [interleave(final[i], final[i+4], 2) for i in range(4)]

        return deinterleaved

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
    """
    A factory function.

    Args:
        filepaths (:obj:`list` of :obj:`str`): A list of the filepath(s) to be used\\
        in (de)interleaving.
        savepaths ()
    """
    return CPS2Format(filepaths, None, savepaths, verbose)

def deinterleave(data, num_bytes):
    """
    Deinterleaves a (:obj:`bytearray`).
    This has some CPS2 specific 'optimizations' based on how the files are grouped.

    Args:
        data (:obj:`bytearray`): the binary data to be deinterleaved.
        num_bytes (int): the number of bytes data is deinterleaved by.

    Returns:
        two :obj:`bytearray`
    """
    evens = []
    odds = []
    deinterleave_s = Struct('c' * num_bytes)
    deinterleave_iter = deinterleave_s.iter_unpack(data)

    for i in deinterleave_iter:
        evens.extend([*i])
        odds.extend([*next(deinterleave_iter)])

    return b''.join(evens), b''.join(odds)

def interleave(file1, file2, num_bytes):
    """
    Interleaves two (:obj:`bytearray`) together.

    Args:
        COME BACK TO THIS ONCE YOU'VE REFACTORED THE HEADER.

    Returns:
        a (:obj:`bytearray`).
    """
    interleaved = []
    interleave_s = Struct('c' * num_bytes)
    file1_iter = interleave_s.iter_unpack(file1)
    file2_iter = interleave_s.iter_unpack(file2)

    for i in file1_iter:
        file2_next = next(file2_iter)
        interleave_temp = [*i, *file2_next]
        interleaved.extend(interleave_temp)

    return  b''.join(interleaved)
