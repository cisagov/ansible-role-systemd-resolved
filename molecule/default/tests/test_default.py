"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_packages(host):
    """Verify that the expected packages are installed/uninstalled."""
    assert host.package(
        "systemd-resolved"
    ).is_installed, "The package systemd-resolved is not installed."
    assert not host.package(
        "resolvconf"
    ).is_installed, "The package resolvconf is installed."


def test_symlink(host):
    """Verify that /etc/resolv.conf is the expected symlink."""
    f = host.file("/etc/resolv.conf")
    assert f.is_symlink, "/etc/resolv.conf is not a symlink."

    if host.system_info.distribution in ["amzn"]:
        # /run/systemd/resolve/stub-resolv.conf is a symlink to
        # /run/systemd/resolve/resolv.conf in AL2023, so the
        # /etc/resolv.conf symlink resolves to the former.
        symlink_target = "/run/systemd/resolve/resolv.conf"
    else:
        symlink_target = "/run/systemd/resolve/stub-resolv.conf"

    assert (
        f.linked_to == symlink_target
    ), f"/etc/resolv.conf is not a symlink to {symlink_target}."


def test_services(host):
    """Verify that the expected services are present."""
    s = host.service("systemd-resolved")
    # This assertion currently fails because of
    # pytest-dev/pytest-testinfra#757.  Once
    # pytest-dev/pytest-testinfra#754 has been merged and a new
    # release is created the following line can be uncommented.
    # assert s.exists, "systemd-resolved service does not exist."
    assert s.is_enabled, "systemd-resolved service is not enabled."
    assert s.is_running, "systemd-resolved service is not running."
