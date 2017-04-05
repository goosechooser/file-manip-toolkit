from abc import ABC, abstractmethod

# point of metaclass is to enforce a 'contract'
# in this case we require subclasses to have:
# interleave_files, deinterleave_file, run

class FileFormatBase(ABC):
    def __init__(self, filepaths, numbytes, savepaths, verbose):
        self._verbose = verbose
        self.verboseprint = print if self._verbose else lambda *a, **k: None
        self._filepaths = filepaths
        self._numbytes = numbytes
        self._savepaths = savepaths

    @abstractmethod
    def interleave_files(self):
        pass

    @abstractmethod
    def deinterleave_file(self):
        pass

    @abstractmethod
    def run(self):
        pass
