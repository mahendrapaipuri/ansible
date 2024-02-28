from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("dir", [
    "/etc/ceems_exporter/",
])
def test_directories(host, dir):
    d = host.file(dir)
    assert d.exists


@pytest.mark.parametrize("file", [
    "/etc/sudoers.d/allow-ipmi-dcmi",
])
def test_files(host, file):
    f = host.file(file)
    assert f.exists


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


def test_systemd_properties(host):
    s = host.service("ceems_exporter")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"
    assert p.get("Environment") == "EMAPS_API_TOKEN=foo"
    assert p.get("AmbientCapabilities") in [None, ""]


@pytest.mark.parametrize("socket", [
    "tcp://127.0.0.1:8080",
    "tcp://127.0.1.1:8080",
])
def test_socket(host, socket):
    assert host.socket(socket).is_listening
