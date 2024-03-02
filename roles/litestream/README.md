# Ansible Role: Litestream

## Description

Deploy [Litestream](https://github.com/benbjohnson/litestream) using ansible.

## Requirements

- Ansible >= 2.9 (It might work on previous versions, but we cannot guarantee it)
- gnu-tar on Mac deployer host (`brew install gnu-tar`)
- Passlib is required when using the basic authentication feature (`pip install passlib[bcrypt]`)

## Role Variables

All variables which can be overridden are stored in [defaults/main.yml](defaults/main.yml) file as well as in [meta/argument_specs.yml](meta/argument_specs.yml).
Please refer to the [collection docs](https://mahendrapaipuri.github.io/ansible/branch/main/litestream_role.html) for description and default values of the variables.

## Example

### Playbook

Use it in a playbook as follows:
```yaml
- hosts: all
  roles:
    - mahendrapaipuri.ansible.litestream
```

### TLS config

Before running litestream role, the user needs to provision their own certificate and key.
```yaml
- hosts: all
  roles:
    - mahendrapaipuri.ansible.litestream
  vars:
    litestream_config:
      dbs:
      - path: /var/lib/db1
        replicas:
          - url: s3://mybkt.litestream.io/db1
```


## Local Testing

The preferred way of locally testing the role is to use Docker and [molecule](https://github.com/ansible-community/molecule) (v3.x). You will have to install Docker on your system. See "Get started" for a Docker package suitable for your system. Running your tests is as simple as executing `molecule test`.

## Continuous Integration

Combining molecule and circle CI allows us to test how new PRs will behave when used with multiple ansible versions and multiple operating systems. This also allows use to create test scenarios for different role configurations. As a result we have quite a large test matrix which can take more time than local testing, so please be patient.

## Contributing

See [contributor guideline](../../CONTRIBUTING.md).

## Troubleshooting

See [troubleshooting](TROUBLESHOOTING.md).

## License

This project is licensed under MIT License. See [LICENSE](../../LICENSE) for more details.
