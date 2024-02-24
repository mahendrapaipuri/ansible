from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_directories(host):
    dirs = []
    for dir in dirs:
        d = host.file(dir)
        assert not d.exists


# def test_service(host):
#     s = host.service("dcgm_exporter")
#     try:
#         assert s.is_running
#     except AssertionError:
#         # Capture service logs
#         journal_output = host.run('journalctl -u dcgm_exporter --since "1 hour ago"')
#         print("\n==== journalctl -u dcgm_exporter Output ====\n")
#         print(journal_output)
#         print("\n============================================\n")
#         raise  # Re-raise the original assertion error


def test_protecthome_property(host):
    s = host.service("dcgm_exporter")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"