"""Module containing the tests for the specify_resolv_conf_target scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_symlink(host):
    """Verify that /etc/resolv.conf is the expected symlink."""
    f = host.file("/etc/resolv.conf")
    assert f.is_symlink, "/etc/resolv.conf is not a symlink."

    symlink_target = "/run/systemd/resolve/resolv.conf"

    assert (
        f.linked_to == symlink_target
    ), f"/etc/resolv.conf is not a symlink to {symlink_target}."


# Unfortunately this test does not function as expected, since Docker
# containers normally just get a copy of their host's /etc/resolv.conf
# and do not receive any DNS nameservers via DHCP.
# @pytest.mark.parametrize(
#     "dig_command",
#     [
#         "www.yahoo.com",
#         "AAAA www.yahoo.com",
#     ],
# )
# def test_dns_resolution(host, dig_command):
#     """Verify that the systemd-resolved resolver is not being used by default."""
#     cmd = host.run(f"dig {dig_command}")
#     assert cmd.rc == 0, f"Command dig {dig_command} did not exit successfully."
#     # Verify that the dig result came from the systemd-resolved
#     # service.
#     assert (
#         re.search(r"^;; SERVER: 127\.0\.0\.53#53", cmd.stdout, re.MULTILINE)
#         is None
#     ), f"Command dig {dig_command} returned a result from 127.0.0.53."
