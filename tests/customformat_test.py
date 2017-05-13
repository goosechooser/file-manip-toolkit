import os
import os.path
import filecmp
import pytest
from file_manip_toolkit.unfman import CustomFormat

# DEINTERLEAVE_FILE = 'cps2_test.13.15.17.19.combined'
TESTDIR = os.path.normpath('tests/test_data/unfman/custom')
KNOWNGOOD = os.path.normpath('tests/test_data/known_good')

INTERLEAVE_FILES = [os.path.join(TESTDIR, name) for name in ['custom_test.0', 'custom_test.1', 'custom_test.2', 'custom_test.3']]
DEINTERLEAVE_FILES = [[os.path.join(TESTDIR, name)] for name in INTERLEAVE_FILES]

GOOD_INTERLEAVED_FILES = [os.path.join(KNOWNGOOD, name) for name in ['custom_combined_2.combined', 'custom_combined_4.combined', 'custom_2_combined_2.combined']]
GOOD_DEINTERLEAVED_FILES = [os.path.join(KNOWNGOOD, name) for name in ['custom_2_combined_2.combined.0', 'custom_2_combined_2.combined.1']]

# @pytest.fixture(params=[2, 4])
# def nsplits(request):
#     return request.param

OUTPUTS = ['testdir\\', 'custom']
@pytest.fixture(params=OUTPUTS)
def outputs(request):
    return request.param

@pytest.mark.parametrize('filepaths, numbytes, expected', [
    (INTERLEAVE_FILES, 2, 1),
    (INTERLEAVE_FILES, 4, 1),
])
def test_interleave_files(filepaths, numbytes, expected, outputs):
    custom = CustomFormat.new(filepaths, numbytes, outputs, False)
    results = custom.interleave_files()
    assert len(results) == expected

@pytest.mark.parametrize('filepaths, numbytes, expected', [
    (INTERLEAVE_FILES, 2, GOOD_INTERLEAVED_FILES[0]),
    (INTERLEAVE_FILES, 4, GOOD_INTERLEAVED_FILES[1]),
    (INTERLEAVE_FILES[:2], 2, GOOD_INTERLEAVED_FILES[2]),
])
def test_run_interleave(tmpdir, filepaths, numbytes, expected, outputs):
    tmp = tmpdir.mkdir(outputs)
    custom = CustomFormat.new(filepaths, numbytes, str(tmp), False)
    custom.run()

    assert len(tmpdir.join(outputs).listdir()) == 1

    for f in tmpdir.join(outputs).listdir():
        assert filecmp.cmp(f.strpath, expected)

@pytest.mark.parametrize('filepaths, numbytes, expected', [
    ([GOOD_INTERLEAVED_FILES[2], '2'], 2, (2, GOOD_DEINTERLEAVED_FILES)),
])
def test_run_deinterleave(tmpdir, filepaths, numbytes, expected, outputs):
    tmp = tmpdir.mkdir(outputs)
    custom = CustomFormat.new(filepaths, numbytes, str(tmp), False)
    custom.run()

    nfiles, goodfiles = expected
    assert len(tmpdir.join(outputs).listdir()) == nfiles

    for i, f in enumerate(tmpdir.join(outputs).listdir()):
        assert filecmp.cmp(f.strpath, goodfiles[i])

def test_run_exception():
    custom = CustomFormat.new('ok', None, None, False)
    with pytest.raises(Exception):
        custom.run()
