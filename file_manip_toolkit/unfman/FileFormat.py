"""
License info here?
"""
from abc import ABC, abstractmethod

# point of metaclass is to enforce a 'contract'
# in this case we require subclasses to have:
# interleave_files, deinterleave_file, run

class FileFormatBase(ABC):
    """Abstract base class representing a file format.
    """
    def __init__(self, filepaths, numbytes, savepaths, verbose):
        self._verbose = verbose
        self.verboseprint = print if self._verbose else lambda *a, **k: None
        self._filepaths = filepaths
        self._numbytes = numbytes
        self._savepaths = savepaths

    @abstractmethod
    def interleave_files(self):
        """
        This method must be overriden.
        """
        raise NotImplementedError

    @abstractmethod
    def deinterleave_file(self):
        """
        This method must be overriden.
        """
        raise NotImplementedError

    @abstractmethod
    def run(self):
        """
        This method must be overriden.
        """
        raise NotImplementedError
