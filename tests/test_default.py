import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')

OMERO = '/opt/omero/web/OMERO.web/bin/omero'


@pytest.mark.parametrize("name", ["omero-web", "nginx"])
def test_services_running_and_enabled(Service, name):
    service = Service(name)
    assert service.is_running
    assert service.is_enabled


def test_omero_web_config(Command, Sudo):
    with Sudo('omeroweb'):
        cfg = Command.check_output("%s config get" % OMERO)
    assert cfg == 'omero.web.server_list=[["localhost", 4064, "molecule"]]'


def test_nginx_gateway(Command):
    out = Command.check_output('curl -L localhost')
    assert 'OMERO.web - Login' in out
