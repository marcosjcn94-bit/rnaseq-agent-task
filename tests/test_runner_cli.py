import subprocess
import sys

def test_runner_cli_is_available_without_docker_execution():
    process=subprocess.run([sys.executable,"-m","benchmark.runner","--help"],capture_output=True,text=True)
    assert process.returncode==0
    assert "--receipt" in process.stdout
