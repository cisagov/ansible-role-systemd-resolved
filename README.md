# ansible-role-systemd-resolved #

[![GitHub Build Status](https://github.com/cisagov/ansible-role-systemd-resolved/workflows/build/badge.svg)](https://github.com/cisagov/ansible-role-systemd-resolved/actions)
[![CodeQL](https://github.com/cisagov/ansible-role-systemd-resolved/workflows/CodeQL/badge.svg)](https://github.com/cisagov/ansible-role-systemd-resolved/actions/workflows/codeql-analysis.yml)

This is an Ansible role that installs and configures
[`systemd-resolved`](https://wiki.archlinux.org/title/systemd-resolved).
It performs the following actions:

- Installs `systemd-resolved` and ensures that `resolvconf` is not
  installed.
- Creates an `/etc/resolv.conf` symlink.
- Optionally disables the `systemd-resolved` stub DNS resolver that
  listens at `127.0.0.53`.

## Requirements ##

None.

## Role Variables ##

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| systemd_resolved_dns_stub_listener | The value to use for the DNSStubListener value in the `systemd-resolved` configuration file.  Must be `tcp`, `udp`, or a boolean value.  See [here](https://man.archlinux.org/man/resolved.conf.5.en) for more information. | `true` | No |
| systemd_resolved_dropin_config_file | The location of the systemd-resolved drop-in configuration file that will be created. | `/etc/systemd/resolved.conf.d/99-ansible-role-systemd-resolved` | No |
| systemd_resolved_resolv_conf_filename | The location of the target to which `/etc/resolv.conf` will be symlinked.  Note that `dynamic_resolv_conf_target_dir` and `static_resolv_conf_target_dir` are role vars that are available for use when defining this variable.  See [here](https://man.archlinux.org/man/systemd-resolved.8#/ETC/RESOLV.CONF) for more information. | `"{{ dynamic_resolv_conf_target_dir }}/stub-resolv.conf"` | No |
<!--
| required_variable | Describe its purpose. | n/a | Yes |
-->

## Dependencies ##

None.

## Installation ##

This role can be installed via the command:

```console
ansible-galaxy install --role-file path/to/requirements.yml
```

where `requirements.yml` looks like:

```yaml
---
- name: systemd_resolved
  src: https://github.com/cisagov/ansible-role-systemd-resolved
```

and may contain other roles as well.

For more information about installing Ansible roles via a YAML file,
please see [the `ansible-galaxy`
documentation](https://docs.ansible.com/ansible/latest/galaxy/user_guide.html#installing-multiple-roles-from-a-file).

## Example Playbook ##

Here's how to use it in a playbook:

```yaml
- hosts: all
  become: true
  become_method: sudo
  tasks:
    - name: Include systemd-resolved
      ansible.builtin.include_role:
        name: systemd_resolved
```

## Contributing ##

We welcome contributions!  Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for
details.

## License ##

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.

## Author Information ##

Shane Frasier - <jeremy.frasier@gwe.cisa.dhs.gov>
