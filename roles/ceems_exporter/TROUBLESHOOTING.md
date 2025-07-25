# Troubleshooting

## Bad requests (HTTP 400)

This role downloads checksums from the Github project to verify the integrity of artifacts installed on your servers. When downloading the checksums, a "bad request" error might occur.

This happens in environments which (knowingly or unknowingly) use the [netrc mechanism](https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html) to auto-login into servers.

Unless netrc is needed by your playbook and ansible roles, please unset the var like so:

```bash
NETRC= ansible-playbook ...
```

Or:

```bash
export NETRC=
ansible-playbook ...
```
