import os
import struct
import pytest
from file_manip_toolkit.eswap import eswap

TESTDATA = bytearray.fromhex("0A 0B 0C 0D")
TESTDATA2 = bytearray.fromhex("0A 0B 0C 0D 0A 0B 0C 0D")
TESTDATA3 = bytearray.fromhex("0A 0B 0C 0D 0A 0B 0C 0D 0A 0B 0C 0D 0A 0B 0C 0D")
TESTFILE = 'testdir\\vm3.15'

def test_swap_h():
    result = eswap.swap(TESTDATA, 'h')
    assert(result) == bytearray.fromhex("0B 0A 0D 0C")
    result2 = eswap.swap(result, 'h')
    assert(result2) == TESTDATA

def test_swap_H():
    result = eswap.swap(TESTDATA, 'H')
    assert(result) == bytearray.fromhex("0B 0A 0D 0C")
    result2 = eswap.swap(result, 'H')
    assert(result2) == TESTDATA

# Check this out - struct.error: bad char in struct format
# def test_swap_e():
#     result = eswap.swap(TESTDATA, 'e')
#     assert(result) == bytearray.fromhex("0B 0A 0D 0C")
#     result2 = eswap.swap(result, 'e')
#     assert(result2) == TESTDATA

def test_swap_i():
    result = eswap.swap(TESTDATA, 'i')
    assert(result) == bytearray.fromhex("0D 0C 0B 0A")
    result2 = eswap.swap(result, 'i')
    assert(result2) == TESTDATA

def test_swap_I():
    result = eswap.swap(TESTDATA, 'I')
    assert(result) == bytearray.fromhex("0D 0C 0B 0A")
    result2 = eswap.swap(result, 'I')
    assert(result2) == TESTDATA

def test_swap_q():
    result = eswap.swap(TESTDATA2, 'q')
    assert(result) == bytearray.fromhex("0D 0C 0B 0A 0D 0C 0B 0A")
    result2 = eswap.swap(result, 'q')
    assert(result2) == TESTDATA2

def test_swap_Q():
    result = eswap.swap(TESTDATA2, 'Q')
    assert(result) == bytearray.fromhex("0D 0C 0B 0A 0D 0C 0B 0A")
    result2 = eswap.swap(result, 'Q')
    assert(result2) == TESTDATA2

def test_swap_exception():
    with pytest.raises(struct.error):
        eswap.swap(TESTDATA, 'Q')

    with pytest.raises(struct.error):
        eswap.swap(TESTDATA, 'e')

# format_filename(filename, savepath, suffix)
def test_format_filename_default():
    result = eswap.format_filename('vm3.15', None, 'swapped')
    assert result == 'vm3.15.swapped'

def test_format_filename_custom():
    result = eswap.format_filename('vm3.15', 'custom', 'swapped')
    assert result == 'custom.swapped'

def test_format_filename_folder(tmpdir):
    fn = tmpdir.mkdir('custom')
    result = eswap.format_filename('vm3.15', str(fn), 'swapped')
    head, tail = os.path.split(result)
    comb_result = '\\'.join([os.path.basename(head), tail])
    assert comb_result == 'custom\\vm3.15.swapped'

    fn2 = fn.join('temp')
    result = eswap.format_filename('vm3.15', str(fn2), 'swapped')
    head, tail = os.path.split(result)
    comb_result = '\\'.join([os.path.basename(head), tail])
    assert comb_result == 'custom\\temp.swapped'

def test_open_file():
    assert eswap.open_file(TESTFILE)

def test_open_file_exception():
    with pytest.raises(FileNotFoundError):
        eswap.open_file('vm3.txt')
