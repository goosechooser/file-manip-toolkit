import sys
import pytest
from file_manip_toolkit.eswap import cli

# todo - parameterize
def test_parse_args():
    args = cli.parse_args(['test.py', 'filetemp', '-o', 'here'])
    assert args.file
    assert args.format
    assert args.output

    with pytest.raises(AssertionError):
        assert args.verbose

@pytest.mark.parametrize("test_input, expected", [
    (['eswap_placeholder', 'test', 'filetemp', '-o', 'here'], 1),
    (['eswap_placeholder', 'testdir\\vm3.13', 'h', '-o', 'there'], 0),
])
def test_main(tmpdir, test_input, expected):
    fn = tmpdir.mkdir('cool').join(test_input[-1])
    new_input = test_input[:-1]
    new_input.append(str(fn))
    sys.argv = new_input
    with pytest.raises(SystemExit) as sysexit:
        cli.main()
        assert sysexit.code == expected
