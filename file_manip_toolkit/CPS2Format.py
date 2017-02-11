import os
from file_manip_toolkit.file_manip import interleave, deinterleave
from file_manip_toolkit.FileFormat import FileFormat

class CPS2Format(FileFormat):
    @staticmethod
    def _reshape(list_):
        zipdata = zip(*list_)

        reshape = []
        for z in zipdata:
            reshape.extend([*z])

        return [reshape[i:i+2] for i in range(0, len(reshape), 2)]

    def run(self):
        if len(self._filepaths) == 1:
            self.deinterleave_file()
        else:
            self.interleave_files()

    def interleave_files(self):
        """Interleaves a set of 4 cps2 graphics files."""

        self.verboseprint('Opening files')
        data = [self.open_file(fp) for fp in self._filepaths]

        self.verboseprint('Splitting files')
        split_data = [deinterleave(fsplit, 2, 2) for fsplit in data]
        # initial split gives us something like:
        # [['13e', '13o'], ['15e', '15o'], ['17e', '17o'], ['19e', '19o']]
        # want it shaped like this:
        # [['13e', '15e'], ['17e', '19e'], ['13o', '15o'], ['17o', '19o']]

        reshaped = self._reshape(split_data)

        self.verboseprint('First pass - interleaving every 2 bytes')
        first_interleave = [interleave(pair, 2) for pair in reshaped]
        reshaped = [first_interleave[i:i+2] for i in range(0, len(first_interleave), 2)]

        self.verboseprint('Second pass - interleaving every 64 bytes')
        second_interleave = [interleave(pair, 64) for pair in reshaped]

        self.verboseprint('Last pass - interleaving every 1048576 bytes')
        final = [interleave(second_interleave, 1048576)]

        #assemble parts for saving the file
        filepaths = [os.path.split(fpath)[1] for fpath in self._filepaths]
        splits = [name.split('.') for name in filepaths]
        bases = [base[0] for base in splits]
        nums = [str(num[1]) for num in splits]

        fname = ['.'.join([bases[0], *nums])]

        self.save(final, fname, ['combined'])

    def deinterleave_file(self):
        """Deinterleaves a interleaved cps2 graphics file."""

        self.verboseprint('Opening files')
        data = self.open_file(self._filepaths[0])

        self.verboseprint('First pass - deinterleaving every 1048576 bytes')
        first = deinterleave(data, 1048576, 2)

        second = []
        self.verboseprint('Second pass - deinterleaving every 64 bytes')
        for half in first:
            second.extend(deinterleave(half, 64, 2))

        final = []
        self.verboseprint('Final pass - deinterleaving every 2 bytes')
        for quarter in second:
            final.extend(deinterleave(quarter, 2, 2))

        deinterleaved = [interleave([final[i], final[i+4]], 2) for i in range(4)]

        #assemble parts for saving the file
        filepaths = [os.path.split(f)[1] for f in self._filepaths]
        splits = filepaths[0].split('.')
        nums = splits[1:]
        fnames = [splits[0]] * 4

        self.save(deinterleaved, fnames, nums)

    def save(self, savedata, filenames, suffixes):
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

        for savepath, data in zip(spaths, savedata):
            with open(savepath, 'wb') as f:
                self.verboseprint('Saving', savepath)
                f.write(data)
