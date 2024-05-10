"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os
import re

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_symlink(host):
    """Verify that /etc/resolv.conf is the expected symlink."""
    f = host.file("/etc/resolv.conf")
    assert f.is_symlink, "/etc/resolv.conf is not a symlink."

    if host.system_info.distribution in ["amzn"]:
        # /run/systemd/resolve/stub-resolv.conf is a symlink to
        # /run/systemd/resolve/resolv.conf in AL2023, so the
        # /etc/resolv.conf symlink resolves to the latter.
        symlink_target = "/run/systemd/resolve/resolv.conf"
    else:
        symlink_target = "/run/systemd/resolve/stub-resolv.conf"

    assert (
        f.linked_to == symlink_target
    ), f"/etc/resolv.conf is not a symlink to {symlink_target}."


@pytest.mark.parametrize(
    "dig_command",
    [
        "www.yahoo.com",
        "AAAA www.yahoo.com",
    ],
)
def test_dns_resolution(host, dig_command):
    """Verify that the systemd-resolved resolver is being used by default."""
    cmd = host.run(f"dig {dig_command}")
    assert cmd.rc == 0, f"Command dig {dig_command} did not exit successfully."
    # AL2023 is funky.  /run/systemd/resolve/stub-resolv.conf is
    # itself a symlink to /run/systemd/resolve/resolv.conf, which
    # points directly to the nameserver obtained from DNS.  I don't
    # know why it does this, but our testing must work around it.
    if host.system_info.distribution in ["amzn"]:
        pass
    else:
        # Verify that the dig result came from the systemd-resolved
        # service.
        assert (
            re.search(r"^;; SERVER: 127\.0\.0\.53#53", cmd.stdout, re.MULTILINE)
            is not None
        ), f"Command dig {dig_command} did not return a results from 127.0.0.53."
