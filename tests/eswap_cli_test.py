import os
import sys
import struct
import pytest
from file_manip_toolkit.eswap import cli


def test_parse_args():
    args = cli.parse_args(['test.py', 'filetemp', '-o', 'here'])
    assert args.file
    assert args.format
    assert args.output

    with pytest.raises(AssertionError):
        assert args.verbose

@pytest.fixture(scope='session')
def temp_dir(tmpdir_factory):
    names = ['test.txt']
    fn = [tmpdir_factory.mktemp('test_dir').join(name) for name in names]
    return [f.write('ok') for f in fn]

@pytest.mark.parametrize("test_input, expected", [
    (['eswap_placeholder', 'test', 'filetemp', '-o', 'here'], 1),
    (['eswap_placeholder', 'testdir\\vm3.13', 'h', '-o', 'there'], 0),
])
def test_main(test_input, expected):
    sys.argv = test_input
    with pytest.raises(SystemExit) as sysexit:
        cli.main()
        assert sysexit.code == expected
