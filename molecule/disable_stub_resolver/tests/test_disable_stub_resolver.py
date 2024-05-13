"""Module containing the tests for the disable_stub_resolver scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_port_53_listener(host):
    """Verify that nothing is listening on port 53."""
    # Have netstat output all TCP and UDP IPv4 listeners.
    netstat_cmd = "netstat --protocol inet --listening --numeric --tcp --udp "
    # Skip the first two lines of the output.
    tail_cmd = "tail --lines +3"
    # Grab only the 4th column.
    awk_cmd = "awk '{print $4}'"
    # Grab only the port.
    cut_cmd = "cut --delimiter ':' --fields 2"
    # Output the number of lines that contain only the number 53.
    grep_cmd = 'grep --count "^53$"'
    cmd = host.run(
        f"test 0 -eq $({netstat_cmd} | {tail_cmd} | {awk_cmd} | {cut_cmd} | {grep_cmd})"
    )
    assert cmd.rc == 0, "Something is listening on port 53."
