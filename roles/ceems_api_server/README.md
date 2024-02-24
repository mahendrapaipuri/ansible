# Ansible Role: CEEMS API server

## Description

Deploy [ceems api server](https://github.com/mahendrapaipuri/ceems) using ansible.

## Requirements

- Ansible >= 2.9 (It might work on previous versions, but we cannot guarantee it)
- gnu-tar on Mac deployer host (`brew install gnu-tar`)
- Passlib is required when using the basic authentication feature (`pip install passlib[bcrypt]`)

## Role Variables

All variables which can be overridden are stored in [defaults/main.yml](defaults/main.yml) file as well as in [meta/argument_specs.yml](meta/argument_specs.yml).
Please refer to the [collection docs](https://mahendrapaipuri.github.io/ansible/branch/main/ceems_api_server_role.html) for description and default values of the variables.

## Example

### Playbook

Use it in a playbook as follows:
```yaml
- hosts: all
  roles:
    - mahendrapaipuri.ansible.ceems_api_server
```

### TLS config

Before running ceems_api_server role, the user needs to provision their own certificate and key.
```yaml
- hosts: all
  pre_tasks:
    - name: Create ceems_api_server cert dir
      file:
        path: "/etc/ceems_api_server"
        state: directory
        owner: root
        group: root

    - name: Create cert and key
      openssl_certificate:
        path: /etc/ceems_api_server/tls.cert
        csr_path: /etc/ceems_api_server/tls.csr
        privatekey_path: /etc/ceems_api_server/tls.key
        provider: selfsigned
  roles:
    - mahendrapaipuri.ansible.ceems_api_server
  vars:
    ceems_api_server_tls_server_config:
      cert_file: /etc/ceems_api_server/tls.cert
      key_file: /etc/ceems_api_server/tls.key
    ceems_api_server_basic_auth_users:
      randomuser: examplepassword
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
