from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_directories(host):
    dirs = [
        "/var/lib/ceems_api_server"
    ]
    for dir in dirs:
        d = host.file(dir)
        assert d.is_directory
        assert d.exists


def test_files(host):
    files = [
        "/etc/systemd/system/ceems_api_server.service",
        "/usr/local/bin/ceems_api_server"
    ]
    for file in files:
        f = host.file(file)
        assert f.exists
        assert f.is_file


def test_permissions_didnt_change(host):
    dirs = [
        "/etc",
        "/root",
        "/usr",
        "/var"
    ]
    for file in dirs:
        f = host.file(file)
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


def test_protecthome_property(host):
    s = host.service("ceems_api_server")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"


def test_socket(host):
    sockets = [
        "tcp://127.0.0.1:9020"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
