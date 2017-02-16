import os
from file_manip_toolkit.unfman import file_manip
from file_manip_toolkit.unfman import FileFormat

class CPS2Format(FileFormat.FileFormat):
    @staticmethod
    def _reshape(list_):
        zipdata = zip(*list_)

        reshape = []
        for z in zipdata:
            reshape.extend([*z])

        return [reshape[i:i+2] for i in range(0, len(reshape), 2)]

    def run(self):
        if len(self._filepaths) == 1:
            final = self.deinterleave_file()
        else:
            final = self.interleave_files()

        savepaths = self.format_filenames()

        self.save(savepaths, final)

    def interleave_files(self):
        """Interleaves a set of 4 cps2 graphics files."""

        self.verboseprint('Opening files')
        data = [file_manip.open_file(fp) for fp in self._filepaths]

        self.verboseprint('Splitting files')
        split_data = [file_manip.deinterleave(fsplit, 2, 2) for fsplit in data]
        # initial split gives us something like:
        # [['13e', '13o'], ['15e', '15o'], ['17e', '17o'], ['19e', '19o']]
        # want it shaped like this:
        # [['13e', '15e'], ['17e', '19e'], ['13o', '15o'], ['17o', '19o']]

        reshaped = self._reshape(split_data)

        self.verboseprint('First pass - interleaving every 2 bytes')
        first_interleave = [file_manip.interleave(pair, 2) for pair in reshaped]
        reshaped = [first_interleave[i:i+2] for i in range(0, len(first_interleave), 2)]

        self.verboseprint('Second pass - interleaving every 64 bytes')
        second_interleave = [file_manip.interleave(pair, 64) for pair in reshaped]

        self.verboseprint('Last pass - interleaving every 1048576 bytes')
        final = [file_manip.interleave(second_interleave, 1048576)]

        return final

    def deinterleave_file(self):
        """Deinterleaves a interleaved cps2 graphics file."""

        self.verboseprint('Opening files')
        data = file_manip.open_file(self._filepaths[0])

        self.verboseprint('First pass - deinterleaving every 1048576 bytes')
        first = file_manip.deinterleave(data, 1048576, 2)

        second = []
        self.verboseprint('Second pass - deinterleaving every 64 bytes')
        for half in first:
            second.extend(file_manip.deinterleave(half, 64, 2))

        final = []
        self.verboseprint('Final pass - deinterleaving every 2 bytes')
        for quarter in second:
            final.extend(file_manip.deinterleave(quarter, 2, 2))

        deinterleaved = [file_manip.interleave([final[i], final[i+4]], 2) for i in range(4)]

        return deinterleaved

    def format_filenames(self):
        print('savepaths is:', self._savepaths)
        if len(self._filepaths) == 1:
            # print("deinterleavE")
            #assemble parts for saving the file
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

        # print('spaths is:', spaths)
        return spaths

    def save(self, savepaths, savedata):
        print('Saving:', savepaths)
        for spath, data in zip(savepaths, savedata):
            with open(spath, 'wb') as f:
                self.verboseprint('Saving', spath)
                f.write(data)

#can remove 'numbytes' from function header
def new(filepaths, numbytes, savepaths, verbose):
    return CPS2Format(filepaths, numbytes, savepaths, verbose)
