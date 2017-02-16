import os
from file_manip_toolkit.helpers import is_number
from file_manip_toolkit.unfman import file_manip, FileFormat

#Other possible names, GenericFormat / NoFormat ?
class CustomFormat(FileFormat.FileFormat):
    def run(self):
        if len(self._filepaths) == 2:
            if is_number(self._filepaths[1]):
                self.nsplit = int(self._filepaths[1])

                final = self.deinterleave_file()

                filenames = [os.path.split(self._filepaths[0])[1]] * self._nsplit
                suffixes = [str(i) for i in range(self._nsplit)]

            else:
                final = self.interleave_files()

                filenames = ['.'.join([os.path.split(fname)[1] for fname in self._filepaths])]
                suffixes = ['combined']

        elif len(self._filepaths) > 2:
            final = self.interleave_files()

            filenames = ['.'.join([os.path.split(fname)[1] for fname in self._filepaths])]
            suffixes = ['combined']

        else:
            print('Something broke - number of filepaths:', len(self._filepaths))
            raise Exception

        self.save(final, filenames, suffixes)

    def interleave_files(self):
        self.verboseprint('Opening files')
        data = [file_manip.open_file(fp) for fp in self._filepaths]

        self.verboseprint('Interleaving files every', self._numbytes, 'bytes')

        return [file_manip.interleave(data, int(self._numbytes))]

    def deinterleave_file(self):
        self.verboseprint('Opening file')
        data = file_manip.open_file(self._filepaths[0])

        self.verboseprint('Deinterleaving file every', self._numbytes, 'bytes')
        self.verboseprint('Producing', self._nsplit, 'files')

        return file_manip.deinterleave(data, int(self._numbytes), self._nsplit)

    def save(self, savedata, filenames, suffixes):
        print('_savepaths:', self._savepaths)
        #if no custom output, save to cwd with default name
        if not self._savepaths:
            fnames = [os.path.split(fname)[1] for fname in filenames]
            spaths = ['.'.join([fname, s]) for fname, s in zip(fnames, suffixes)]

        #if custom output is a folder, save default file name to that location
        elif os.path.isdir(self._savepaths):
            head = self._savepaths
            # print('filenames is:', filenames)
            tails = ['.'.join([fname, s]) for fname, s in zip(filenames, suffixes)]
            # print('tails is:', tails)
            spaths = [os.path.join(head, tail) for tail in tails]

        #if custom output is a file, append number to the end of it
        else:
            spaths = ['.'.join([self._savepaths, s]) for s in suffixes]
        
        print('spaths:', spaths)
        for savepath, data in zip(spaths, savedata):
            with open(savepath, 'wb') as f:
                self.verboseprint('Saving', savepath)
                f.write(data)

# Factory method
def new(filepaths, numbytes, savepaths, verbose):
    return CustomFormat(filepaths, numbytes, savepaths, verbose)
