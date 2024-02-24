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


@pytest.mark.parametrize("files", [
    "/etc/systemd/system/dcgm_exporter.service",
    "/usr/local/bin/dcgm_exporter"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file
