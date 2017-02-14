import struct
import pytest
from file_manip_toolkit import file_manip

TESTDATA = bytearray.fromhex('0A 0B 0C 0D A0 B0 C0 D0')
TESTDATA2 = bytearray.fromhex('FA FB FC FD AF BF CF DF')

TESTFILE = 'testdir\\vm3.15'

def test_deinterleave():
    result = file_manip.deinterleave(TESTDATA, 1, 2)
    assert result[0] == bytearray.fromhex('0A 0C A0 C0')
    assert result[1] == bytearray.fromhex('0B 0D B0 D0')

    result = file_manip.deinterleave(TESTDATA, 2, 2)
    assert result[0] == bytearray.fromhex('0A 0B A0 B0')
    assert result[1] == bytearray.fromhex('0C 0D C0 D0')

    #more tests related nbytes/nsplit?

def test_deinterleave_exception():
    with pytest.raises(struct.error):
        file_manip.deinterleave(TESTDATA, 3, 2)
        file_manip.deinterleave(TESTDATA, 99, 2)
        file_manip.deinterleave(TESTDATA, 99, 2)
        file_manip.deinterleave(TESTDATA, 8, 1)
        file_manip.deinterleave(TESTDATA, 1, 1)

def test_interleave():
    result = file_manip.interleave([TESTDATA, TESTDATA2], 2)
    assert result == bytearray.fromhex('0A 0B FA FB 0C 0D FC FD A0 B0 AF BF C0 D0 CF DF')

    result = file_manip.interleave([TESTDATA, TESTDATA2], 4)
    assert result == bytearray.fromhex('0A 0B 0C 0D FA FB FC FD A0 B0 C0 D0 AF BF CF DF')

def test_interleave_exception():
    with pytest.raises(struct.error):
        file_manip.interleave([TESTDATA, TESTDATA2], 99)

def test_open_file():
    assert file_manip.open_file(TESTFILE)

def test_open_file_exception(tmpdir):
    fn = tmpdir.mkdir('data')

    with pytest.raises(OSError):
        file_manip.open_file(str(fn))

    with pytest.raises(FileNotFoundError):
        file_manip.open_file("vm.txt")
