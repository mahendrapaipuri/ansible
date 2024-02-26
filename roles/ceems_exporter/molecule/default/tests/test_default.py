from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("file", [
    "/etc/systemd/system/ceems_exporter.service", 
    "/usr/local/bin/ceems_exporter"
])
def test_files(host, file):
    f = host.file(file)
    assert f.exists
    assert f.is_file


@pytest.mark.parametrize("dir", [
    "/etc",
    "/root",
    "/usr",
    "/var"
])
def test_permissions_didnt_change(host, dir):
    f = host.file(dir)
    assert f.exists
    assert f.is_directory
    assert f.user == "root"
    assert f.group == "root"


def test_user(host):
    assert host.group("ceemsexp").exists
    assert "ceemsexp" in host.user("ceemsexp").groups
    assert host.user("ceemsexp").shell == "/usr/sbin/nologin"
    assert host.user("ceemsexp").home == "/"


def test_service(host):
    s = host.service("ceems_exporter")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u ceems_exporter --since "1 hour ago"')
        print("\n==== journalctl -u ceems_exporter Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


def test_protecthome_property(host):
    s = host.service("ceems_exporter")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"


@pytest.mark.parametrize("socket", [
    "tcp://127.0.0.1:9010",
])
def test_socket(host, socket):
    s = host.socket(socket)
    assert s.is_listening
