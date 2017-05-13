import os
import os.path
import sys
import pytest
from file_manip_toolkit.unfman import cli


custom_dir = os.path.normpath('tests/test_data/unfman/')
custom_ifiles = ['cps2_test.13', 'cps2_test.15', 'cps2_test.17', 'cps2_test.19']
custom_interleave = [os.path.join(custom_dir, name) for name in custom_ifiles]

custom_dfiles = ['cps2_test.13.15.17.19.combined']
custom_deinterleave = [[os.path.join(custom_dir, name), '4'] for name in custom_dfiles]
cps2_deinterleave = [os.path.join(custom_dir, name) for name in custom_dfiles]

@pytest.fixture(params=[*custom_deinterleave, 
                        custom_interleave, custom_interleave[:2], custom_interleave[1:]])
def files(request):
    return request.param

@pytest.fixture(params=[cps2_deinterleave, custom_interleave])
def cps2files(request):
    return request.param

@pytest.fixture(params=['2', '4'])
def nbytes(request):
    return request.param

@pytest.fixture(params=[['-o', 'here'], [' ']])
def output(request):
    return request.param


@pytest.fixture(params=[['-v'], ['--verbose']])
def verbose(request):
    return request.param

# error occurs if trying to use [''] or [' '] as the last character
# not sure if valid test/issue?
def test_parse_args(files, nbytes, output, verbose):
    args = cli.parse_args([*files, nbytes, *output, *verbose])
    assert args.files
    assert args.numbytes

def test_main_custom(tmpdir, files, nbytes, output, verbose):
    if output[0] == '-o':
        fn = tmpdir.mkdir(output[-1])
        newoutput = [output[0], str(fn)]
    else:
        newoutput = output[-1]

    sys.argv = ['unfman', *files, nbytes, *newoutput, *verbose]
    print(sys.argv)

    with pytest.raises(SystemExit) as sysexit:
        cli.main()
        assert sysexit.code == 0

def test_main_cps2(tmpdir, cps2files, output, verbose):
    if output[0] == '-o':
        fn = tmpdir.mkdir(output[-1])
        newoutput = [output[0], str(fn)]
    else:
        newoutput = output[-1]

    sys.argv = ['unfman', *cps2files, 'cps2', *newoutput, *verbose]
    with pytest.raises(SystemExit) as sysexit:
        cli.main()
        assert sysexit.code == 0

