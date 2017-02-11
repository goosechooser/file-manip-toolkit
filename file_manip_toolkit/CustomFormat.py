import os
from file_manip_toolkit.file_manip import interleave, deinterleave, open_file, is_number
from file_manip_toolkit.FileFormat import FileFormat

#Other possible names, GenericFormat / NoFormat ?
class CustomFormat(FileFormat):
    def run(self):
        if len(self._filepaths) == 2:
            if is_number(self._filepaths[1]):
                self.nsplit = int(self._filepaths[1])
                self.deinterleave_file()
            else:
                self.interleave_files()
        elif len(self._filepaths) > 2:
            self.interleave_files()
        else:
            print('Something broke')

    def interleave_files(self):
        self.verboseprint('Opening files')
        data = [open_file(fp) for fp in self._filepaths]

        self.verboseprint('Interleaving files every', self._numbytes, 'bytes')
        interleave_data = [interleave(data, self._numbytes)]

        filename = ['.'.join([os.path.split(fname)[1] for fname in self._filepaths])]
        suffix = ['combined']

        self.save(interleave_data, filename, suffix)

    def deinterleave_file(self):
        self.verboseprint('Opening file')
        data = open_file(self._filepaths[0])

        self.verboseprint('Deinterleaving file every', self._numbytes, 'bytes')
        self.verboseprint('Producing', self._nsplit, 'files')
        deinterleave_data = deinterleave(data, self._numbytes, self._nsplit)

        filenames = [os.path.split(self._filepaths[0])[1]] * self._nsplit
        suffixes = [str(i) for i in range(self._nsplit)]

        self.save(deinterleave_data, filenames, suffixes)

    def save(self, savedata, filenames, suffixes):
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

        for savepath, data in zip(spaths, savedata):
            with open(savepath, 'wb') as f:
                self.verboseprint('Saving', savepath)
                f.write(data)
