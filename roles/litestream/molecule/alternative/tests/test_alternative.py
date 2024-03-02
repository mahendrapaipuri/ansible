from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("dir", [
    "/etc/litestream",
    "/var/lib/backup_sample",
    "/var/lib/backup_sample/generations",
    "/nfs/db/backups/backup_sample",
    "/nfs/db/backups/backup_sample/generations",
])
def test_directories(host, dir):
    d = host.file(dir)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("file", [
    "/etc/systemd/system/litestream.service",
    "/etc/litestream/config.yml",
])
def test_files(host, file):
    f = host.file(file)
    assert f.exists
    assert f.is_file


@pytest.mark.parametrize("file", [
    "/etc",
    "/root",
    "/usr",
    "/var"
])
def test_permissions_didnt_change(host, file):
    f = host.file(file)
    assert f.exists
    assert f.is_directory
    assert f.user == "root"
    assert f.group == "root"


def test_user(host):
    assert host.group("litestream").exists
    assert "litestream" in host.user("litestream").groups
    assert host.user("litestream").shell == "/usr/sbin/nologin"
    assert host.user("litestream").home == "/"


def test_service(host):
    s = host.service("litestream")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u litestream --since "1 hour ago"')
        print("\n==== journalctl -u litestream Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


def test_systemd_properties(host):
    s = host.service("litestream")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"
