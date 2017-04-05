import struct
import pytest
from file_manip_toolkit.unfman.CustomFormat import CustomFormat, interleave, deinterleave

# This is probably gonna get deleted/moved to other places

TESTDATA = bytearray.fromhex('0A 0B 0C 0D A0 B0 C0 D0')
TESTDATA2 = bytearray.fromhex('FA FB FC FD AF BF CF DF')

TESTFILE = 'testdir\\vm3.15'

@pytest.mark.parametrize('test_input, nsplit, expected', [
    (TESTDATA, 1, ('0A 0C A0 C0', '0B 0D B0 D0')),
    (TESTDATA, 2, ('0A 0B A0 B0', '0C 0D C0 D0')),
])
def test_deinterleave(test_input, nsplit, expected):
    result = deinterleave(test_input, nsplit, 2)
    assert result[0] == bytearray.fromhex(expected[0])
    assert result[1] == bytearray.fromhex(expected[1])

#todo - figure out what exception the following cases are raising
#(TESTDATA, 8, 2),
#(TESTDATA, 1, 1),
@pytest.mark.parametrize('test_input, nbytes, nsplit', [
    (TESTDATA, 3, 2),
    (TESTDATA, 99, 2),
])
def test_deinterleave_exception(test_input, nbytes, nsplit):
    with pytest.raises(struct.error):
        deinterleave(test_input, nbytes, nsplit)

@pytest.mark.parametrize('test_input, nsplit, expected', [
    ([TESTDATA, TESTDATA2], 2, '0A 0B FA FB 0C 0D FC FD A0 B0 AF BF C0 D0 CF DF'),
    ([TESTDATA, TESTDATA2], 4, '0A 0B 0C 0D FA FB FC FD A0 B0 C0 D0 AF BF CF DF'),
])
def test_interleave(test_input, nsplit, expected):
    result = interleave(test_input, nsplit)
    assert result == bytearray.fromhex(expected)

def test_interleave_exception():
    with pytest.raises(struct.error):
        interleave([TESTDATA, TESTDATA2], 99)

def test_open_file():
    assert CustomFormat.open_file(TESTFILE)

def test_open_file_exception(tmpdir):
    fn = tmpdir.mkdir('data')

    with pytest.raises(OSError):
        CustomFormat.open_file(str(fn))

    with pytest.raises(FileNotFoundError):
        CustomFormat.open_file("vm.txt")
