from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("files", [
    "/etc/systemd/system/ceems_exporter.service",
    "/usr/local/bin/ceems_exporter"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


def test_directories(host):
    dirs = []
    for dir in dirs:
        d = host.file(dir)
        assert d.is_directory
        assert d.exists


def test_capabilities_property(host):
    s = host.service("ceems_exporter")
    p = s.systemd_properties
    assert p.get("AmbientCapabilities") == "cap_dac_read_search cap_sys_ptrace"


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


def test_socket(host):
    s = host.socket("tcp://0.0.0.0:9010")
    assert s.is_listening


def test_collectors(host):
    exporter_out = host.check_output('curl http://localhost:9010/metrics').strip()
    assert "ceems_scrape_collector_success{collector=\"ipmi_dcmi\"}" not in exporter_out
    assert "ceems_scrape_collector_success{collector=\"rapl\"}" not in exporter_out
    assert "ceems_scrape_collector_success{collector=\"emissions\"}" in exporter_out
