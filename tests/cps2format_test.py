import os
import filecmp
import pytest
from file_manip_toolkit.unfman import CPS2Format

TESTDIR = 'tests\\testdir'
FILES = ['vm3.13', 'vm3.15', 'vm3.17', 'vm3.19']
PREFIX = 'known_good'
GOODFILES = ['\\'.join([PREFIX, fname]) for fname in FILES]
DEINTERLEAVE_FILE = 'tests\\testdir\\known_good\\cps2_test.13.15.17.19.combined'

NBYTES = [2, 4]
NSPLITS = [2, 4]
OUTPUTS = ['', 'testdir\\', 'testdir\\custom']

@pytest.fixture
def cps2_inter(output):
    files = ['\\'.join([TESTDIR, PREFIX, fname]) for fname in FILES]
    return CPS2Format.new(files, None, output, False)

@pytest.fixture(params=NBYTES)
def numbytes(request):
    return request.param

@pytest.fixture(params=NSPLITS)
def nsplits(request):
    return request.param

@pytest.fixture(params=OUTPUTS)
def outputs(request):
    return request.param

# @pytest.fixture(params=[FILES, [DEINTERLEAVE_FILE]])
# def filepaths(request):
#     return request.param

@pytest.fixture
def temp_dirs(tmpdir_factory, outputs):
    return [str(tmpdir_factory.mktemp(name)) for name in outputs]

# @pytest.mark.parametrize("test_input, expected", [
#     (['eswap_placeholder', 'test', 'filetemp', '-o', 'here'], -1),
#     (['eswap_placeholder', 'testdir\\vm3.13', 'h', '-o', 'there'], 0),
# ])

@pytest.mark.parametrize('filepaths, expected', [
    (FILES, 1),
    ([DEINTERLEAVE_FILE], 4),
])
def test_format_filenames(filepaths, expected, outputs):
    cps2 = CPS2Format.new(filepaths, None, outputs, False)
    results = cps2.format_filenames()
    assert len(results) == expected
