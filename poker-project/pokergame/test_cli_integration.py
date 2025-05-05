import subprocess, sys, textwrap

def test_cli_quick_exit(tmp_path):
    cmd = [sys.executable, "-m", "pokergame.poker"]
    # feed: 2 players → immediately quit at replay prompt
    user_input = textwrap.dedent("""\
        2
        n
    """).encode()
    p = subprocess.run(cmd, input=user_input, capture_output=True, timeout=5)
    assert p.returncode == 0
    assert b"Winner" in p.stdout