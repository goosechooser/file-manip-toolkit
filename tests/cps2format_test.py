import os
import os.path
import filecmp
import pytest
from file_manip_toolkit.unfman import CPS2Format

TESTDIR = 'tests\\testdir'
DEINTERLEAVE_FILE = 'cps2_test.13.15.17.19.combined'
INTERLEAVE_FILES = ['cps2_test.13', 'cps2_test.15', 'cps2_test.17', 'cps2_test.19']
CUSTOM_FILES = ['custom.13', 'custom.15', 'custom.17', 'custom.19']

# tests work for the most part
# but some thought should be given to refactoring them
# maybe

@pytest.fixture(params=[2, 4])
def numbytes(request):
    return request.param

@pytest.fixture(params=[2, 4])
def nsplits(request):
    return request.param

@pytest.fixture(params=['testdir\\', 'custom'])
def outputs(request):
    return request.param

@pytest.mark.parametrize('filepaths, outputs, expected', [
    (INTERLEAVE_FILES, '', (1, [DEINTERLEAVE_FILE])),
    (INTERLEAVE_FILES, 'testdir/', (1, [''.join(['testdir/', DEINTERLEAVE_FILE])])),
    (INTERLEAVE_FILES, 'testdir/custom', (1, ['testdir/custom.combined'])),
    ([DEINTERLEAVE_FILE], '', (4, INTERLEAVE_FILES)),
    ([DEINTERLEAVE_FILE], 'testdir/',
     (4, [''.join(['testdir/', name]) for name in INTERLEAVE_FILES])),
    ([DEINTERLEAVE_FILE], 'testdir/custom',
     (4, [''.join(['testdir/', name]) for name in CUSTOM_FILES])),
])
def test_format_filenames(filepaths, outputs, expected):
    cps2 = CPS2Format.new(filepaths, None, outputs, False)
    results = cps2.format_filenames()
    numfiles, filenames = expected
    assert len(results) == numfiles
    assert results == filenames

# deinterleave runs slower during testing - find out why?
# DOESNT WORK WITH empty case?'' not sure how to test
@pytest.mark.parametrize('test_data, expected', [
    ([''.join(['tests/testdir/', DEINTERLEAVE_FILE])], 4),
    ([''.join(['tests/testdir/', name]) for name in INTERLEAVE_FILES], 1),
])
def test_run(test_data, expected, outputs, tmpdir):
    fns = tmpdir.mkdir(outputs)

    cps2 = CPS2Format.new(test_data, None, str(fns), False)
    cps2.run()

    assert len(tmpdir.join(outputs).listdir()) == expected

    for f in tmpdir.join(outputs).listdir():
        assert filecmp.cmp(f.strpath, os.path.join(TESTDIR, f.basename))