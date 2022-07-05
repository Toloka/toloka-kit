import pathlib
import subprocess


def test_stubs_can_be_generated(tmpdir_factory):
    make_stubs_path = pathlib.Path(__file__).parent.parent / 'bin' / 'make_stubs'
    args = subprocess.run(['sh', str(make_stubs_path / "tolokakit_args.sh")], stdout=subprocess.PIPE, text=True)
    args = _replace_output_dir_with_tmp_dir(args, tmpdir_factory)

    process = subprocess.run(
        ['python', str(make_stubs_path), *args],
        stderr=subprocess.PIPE, text=True,
    )
    if process.returncode != 0:
        assert process.stderr == ''
        raise subprocess.CalledProcessError(process.returncode, process.args)


def _replace_output_dir_with_tmp_dir(args, tmpdir_factory):
    args = args.stdout.split()
    output_dir_idx = args.index('--output-dir')
    args = args[:output_dir_idx + 1] + args[:output_dir_idx + 2]
    output_path = str(tmpdir_factory.mktemp('output'))
    args.insert(output_dir_idx + 1, output_path)
    return args
