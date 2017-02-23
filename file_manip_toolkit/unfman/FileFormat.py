import sys
from abc import ABCMeta, abstractmethod

# point of metaclass is to enforce a 'contract'
# in this case we require subclasses to have:
# interleave_files, deinterleave_file, run

class FileFormat(object, metaclass=ABCMeta):
    def __init__(self, filepaths, numbytes, savepaths, verbose):
        self._verbose = verbose
        self.verboseprint = print if self._verbose else lambda *a, **k: None
        self._filepaths = filepaths
        self._numbytes = numbytes
        self._savepaths = savepaths
        self._nsplit = None

    @abstractmethod
    def interleave_files(self):
        pass

    @abstractmethod
    def deinterleave_file(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @property
    def nsplit(self):
        return self._nsplit

    @nsplit.setter
    def nsplit(self, value):
        self._nsplit = value

    @staticmethod
    def open_file(filepath):
        """Error handling. Returns bytearray of data in file"""
        try:
            with open(filepath, 'rb') as f:
                return bytearray(f.read())
        except FileNotFoundError as error:
            print('Error occured during opening of file:', error, file=sys.stderr)
            raise error

    def save(self, savepaths, savedata):
        for spath, data in zip(savepaths, savedata):
            with open(spath, 'wb') as f:
                self.verboseprint('Saving', spath)
                f.write(data)
