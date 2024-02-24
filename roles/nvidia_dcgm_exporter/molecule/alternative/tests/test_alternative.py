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
    "/etc/dcgm_exporter/counters.csv",
    "/etc/dcgm_exporter/config.yaml",
])
def test_files(host, file):
    f = host.file(file)
    assert f.exists
    assert f.is_file


def test_protecthome_property(host):
    s = host.service("dcgm_exporter")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"
