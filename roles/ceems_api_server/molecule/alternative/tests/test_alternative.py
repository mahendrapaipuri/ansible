from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("dir", [
    "/var/lib/ceems_api_server",
    "/tmp/ceems_api_server"
])
def test_directories(host, dir):
    d = host.file(dir)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("file", [
    "/etc/systemd/system/ceems_api_server.service",
    "/usr/local/bin/ceems_api_server",
    "/etc/ceems_api_server/config.yaml",
    "/etc/ceems_api_server/tsdb_config.yaml",
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
    assert host.group("ceems").exists
    assert "ceems" in host.user("ceems").groups
    assert host.user("ceems").shell == "/usr/sbin/nologin"
    assert host.user("ceems").home == "/"


def test_service(host):
    s = host.service("ceems_api_server")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u ceems_api_server --since "1 hour ago"')
        print("\n==== journalctl -u ceems_api_server Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


def test_systemd_properties(host):
    s = host.service("ceems_api_server")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"
    assert p.get("Environment") == "foo=bar"


@pytest.mark.parametrize("socket", [
    "tcp://127.0.0.1:8080"
])
def test_socket(host, socket):
    s = host.socket(socket)
    assert s.is_listening
