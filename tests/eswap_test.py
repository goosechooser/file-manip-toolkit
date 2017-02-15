import os
import struct
import pytest
from file_manip_toolkit.eswap import eswap

TESTDATA = bytearray.fromhex("0A 0B 0C 0D")
TESTDATA2 = bytearray.fromhex("0A 0B 0C 0D 0A 0B 0C 0D")
TESTDATA3 = bytearray.fromhex("0A 0B 0C 0D 0A 0B 0C 0D 0A 0B 0C 0D 0A 0B 0C 0D")
TESTFILE = 'testdir\\vm3.15'

@pytest.mark.parametrize("test_input, fmt, expected", [
    (TESTDATA, 'h', bytearray.fromhex("0B 0A 0D 0C")),
    (TESTDATA, 'H', bytearray.fromhex("0B 0A 0D 0C")),
    (TESTDATA, 'i', bytearray.fromhex("0D 0C 0B 0A")),
    (TESTDATA, 'I', bytearray.fromhex("0D 0C 0B 0A")),
    (TESTDATA2, 'q', bytearray.fromhex("0D 0C 0B 0A 0D 0C 0B 0A")),
    (TESTDATA2, 'Q', bytearray.fromhex("0D 0C 0B 0A 0D 0C 0B 0A")),
])
def test_swap(test_input, fmt, expected):
    assert eswap.swap(test_input, fmt) == expected
    
@pytest.mark.parametrize("fmt", [
    ('Q'),
    ('e')
])
def test_swap_exception(fmt):
    with pytest.raises(struct.error):
        eswap.swap(TESTDATA, fmt)

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
