from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("dir", [
    "/etc/dcgm_exporter",
])
def test_directories(host, dir):
    d = host.file(dir)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("file", [
    "/etc/systemd/system/dcgm_exporter.service",
    "/usr/local/bin/dcgm_exporter",
    "/etc/dcgm_exporter/counters.csv"
])
def test_files(host, file):
    f = host.file(file)
    assert f.exists
    assert f.is_file


@pytest.mark.parametrize("dir", [
    "/etc",
    "/root",
    "/usr",
    "/var",
])
def test_permissions_didnt_change(host, dir):
    f = host.file(dir)
    assert f.exists
    assert f.is_directory
    assert f.user == "root"
    assert f.group == "root"


def test_user(host):
    assert host.group("dcgmexp").exists
    assert "dcgmexp" in host.user("dcgmexp").groups
    assert host.user("dcgmexp").shell == "/usr/sbin/nologin"
    assert host.user("dcgmexp").home == "/"


def test_protecthome_property(host):
    s = host.service("dcgm_exporter")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"


# Service will run only if GPU drivers are available
# def test_socket(host):
#     sockets = [
#         "tcp://127.0.0.1:9010"
#     ]
#     for socket in sockets:
#         s = host.socket(socket)
#         assert s.is_listening
