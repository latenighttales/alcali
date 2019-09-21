import time
import pytest
from django.contrib.auth.models import User

from api.models import SaltReturns, Jids, Keys, Minions, Schedule, Conformity


@pytest.fixture
def jwt(admin_client):
    res = admin_client.post(
        "/api/token/", data={"username": "admin", "password": "password"}
    )
    token = res.data["access"]
    return {"HTTP_AUTHORIZATION": "Bearer {}".format(token)}


@pytest.fixture
def jid():
    Jids.objects.create(
        jid="20190429180928455927",
        load='{"tgt_type": "glob", "jid": "20190429180928455927", '
        '"tgt": "2e220fd40bc5", "cmd": "publish", "ret": "", '
        '"user": "admin", "key": '
        '"N6TS4++wIWU/7jOQsSYO+E42VbFc/b/j3nD9GC24Oo08jF'
        '/bY49vgksEHUMmRNzLXTuzsdiYLwM=", "kwargs": {"token": '
        '"3ee91b11a58f8265c26db179dd61244b12db375d9855d4b2487033f7'
        '540710ca", "client": "local", "batch": null}, "fun": '
        '"state.apply", "arg": []}',
    )


@pytest.fixture
def key():
    Keys.objects.create(
        minion_id="2e220fd40bc5",
        pub="d5:20:87:6f:85:4c:51:52:9e:63:08:45:04:fd:61:d8:53:5b:c8"
        ":15:08:21:d3:6a:85:8e:27:0b:e8:d4:93:e9",
        status="accepted",
    )


@pytest.fixture
def highstate():
    def _highstate(minion="2e220fd40bc5"):
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        ret = SaltReturns.objects.create(
            fun="state.apply",
            jid="20190429180928455927",
            return_field='{"pkg_|-common_packages_'
            '|-common_packages_|-installed": {'
            '"comment": "The following packages '
            "were "
            "installed/updated: strace, htop, "
            'vim", '
            '"name": "common_packages", '
            '"start_time": '
            '"18:09:30.691635", "result": true, '
            '"duration": 25031.334, '
            '"__run_num__": 0, '
            '"__sls__": "common.packages", '
            '"changes": '
            '{"vim-common": {"new": '
            '"2:8.0.0197-4+deb9u1", "old": ""}, '
            '"strace": {"new": "4.15-2", "old": '
            '""}, '
            '"libgpm2": {"new": "1.20.4-6.2+b1", '
            '"old": ""}, "vim": {"new": '
            '"2:8.0.0197-4+deb9u1", "old": ""}, '
            '"htop": {"new": "2.0.2-1", "old": '
            '""}, '
            '"xxd": {"new": '
            '"2:8.0.0197-4+deb9u1", '
            '"old": ""}, "vim-runtime": {"new": '
            '"2:8.0.0197-4+deb9u1", "old": ""}}, '
            '"__id__": "common_packages"}}',
            id="2e220fd40bc5",
            success=1,
            full_ret='{"fun_args": [], "jid": '
            '"20190429180928455927", "return": {'
            '"pkg_|-common_packages_|-common_packages_'
            '|-installed": {"comment": "The following '
            "packages were installed/updated: strace, "
            'htop, vim", "name": "common_packages", '
            '"start_time": "18:09:30.691635", '
            '"result": '
            'true, "duration": 25031.334, '
            '"__run_num__": '
            '0, "__sls__": "common.packages", '
            '"changes": { '
            '"vim-common": {"new": '
            '"2:8.0.0197-4+deb9u1", '
            '"old": ""}, "strace": {"new": "4.15-2", '
            '"old": ""}, "libgpm2": {"new": '
            '"1.20.4-6.2+b1", "old": ""}, "vim": {'
            '"new": '
            '"2:8.0.0197-4+deb9u1", "old": ""}, '
            '"htop": { '
            '"new": "2.0.2-1", "old": ""}, "xxd": {'
            '"new": '
            '"2:8.0.0197-4+deb9u1", "old": ""}, '
            '"vim-runtime": {"new": '
            '"2:8.0.0197-4+deb9u1", '
            '"old": ""}}, "__id__": '
            '"common_packages"}}, '
            '"retcode": 0, "success": true, '
            '"cmd": "_return", "_stamp": '
            '"2019-04-29T18:09:55.727933", '
            '"fun": "state.apply", "id": '
            '"2e220fd40bc5", '
            '"out": "highstate"}',
            alter_time=date,
        )
        return ret

    return _highstate


@pytest.fixture
def highstate_diff():
    ret = SaltReturns.objects.create(
        fun="state.apply",
        jid="20190507190955945843",
        return_field='{"pkg_|-common_packages_'
        '|-common_packages_|-installed": {'
        '"comment": "The following packages '
        "would "
        'be installed/updated: vim", "name": '
        '"common_packages", "start_time": '
        '"19:09:59.565546", "result": null, '
        '"duration": 412.241, "__run_num__": '
        "0, "
        '"__sls__": "common.packages", '
        '"changes": '
        '{}, "__id__": "common_packages"}, '
        '"pkg_|-install_alcali_'
        "|-install_alcali_ "
        '|-installed": {"comment": "All '
        "specified "
        'packages are already installed", '
        '"name": '
        '"curl", "start_time": '
        '"19:09:59.978059", '
        '"result": true, "duration": 34.526, '
        '"__run_num__": 1, "__sls__": '
        '"alcali", '
        '"changes": {}, "__id__": '
        '"install_alcali"}}',
        id="2e220fd40bc5",
        success=1,
        full_ret='{"fun_args": ["test=True"], "jid": '
        '"20190507190955945843", "return": {'
        '"pkg_|-common_packages_|-common_packages_'
        '|-installed": {"comment": "The following '
        "packages would be installed/updated: "
        'vim", '
        '"name": "common_packages", "start_time": '
        '"19:09:59.565546", "result": null, '
        '"duration": 412.241, "__run_num__": 0, '
        '"__sls__": "common.packages", '
        '"changes": {}, '
        '"__id__": "common_packages"}, '
        '"pkg_|-install_alcali_|-install_alcali_'
        '|-installed": {"comment": "All specified '
        'packages are already installed", "name": '
        '"curl", "start_time": "19:09:59.978059", '
        '"result": true, "duration": 34.526, '
        '"__run_num__": 1, "__sls__": "alcali", '
        '"changes": {}, "__id__": '
        '"install_alcali"}}, '
        '"retcode": 0, "success": true, '
        '"cmd": "_return", "_stamp": '
        '"2019-05-07T19:10:00.018461", '
        '"fun": "state.apply", "id": "master", '
        '"out": "highstate"}',
        alter_time="2019-05-07 19:10:00",
    )
    return ret


@pytest.fixture
def minion():
    minion = Minions.objects.create(
        minion_id="2e220fd40bc5", grain="thisisnotvalid", pillar="same"
    )
    return minion


@pytest.fixture
def dummy_jid():
    Jids.objects.create(
        jid="20190507190955945844",
        load='{"tgt_type": "glob", "jid": "20190507190955945844", '
        '"tgt": "master", "cmd": "publish", "ret": "", '
        '"user": "user1", "key": '
        '"N6TS4++wIWU/7jOQsSYO+E42VbFc/b/j3nD9GC24Oo08jF'
        '/bY49vgksEHUMmRNzLXTuzsdiYLwM=", "kwargs": {"token": '
        '"3ee91b11a58f8265c26db179dd61244b12db375d9855d4b2487033f7'
        '540710ca", "client": "local", "batch": null}, "fun": '
        '"alcali.pass_salt", "arg": []}',
    )


@pytest.fixture
def dummy_state():
    ret = SaltReturns.objects.create(
        fun="alcali.pass_salt",
        jid="20190507190955945844",
        return_field='{"oh": "no"}',
        id="master",
        success=1,
        full_ret='{"return": "noice"}',
        alter_time=time.strftime("%Y-%m-%d %H:%M:%S"),
    )
    return ret


@pytest.fixture
def minion_master():
    ret = Minions.objects.create(
        minion_id="master",
        grain='{"biosversion": "1.5.1", "kernel": "Linux", '
        '"domain": "", "uid": 0, "zmqversion": "4.2.1", '
        '"kernelrelease": "5.0.11-300.fc30.x86_64", '
        '"pythonpath": ['
        '"/usr/lib/python2.7/dist-packages/git/ext'
        '/gitdb", "/usr/bin", "/usr/lib/python2.7", '
        '"/usr/local/lib/python2.7/dist-packages", '
        '"/usr/lib/python2.7/dist-packages", '
        '"/usr/lib/python2.7/dist-packages/gitdb/ext'
        '/smmap"], "serialnumber": "HSZHST2", '
        '"pid": 59, "fqdns": [], "ip_interfaces": {'
        '"lo": ["127.0.0.1"], "eth0": ["172.29.0.4"]}, '
        '"groupname": "root", "fqdn_ip6": [], '
        '"mem_total": 15480, "saltversioninfo": [2019, '
        '2, 0, 0], "zfs_support": false, "SSDs": ['
        '"dm-1", "nvme0n1", "dm-2", "dm-0", "dm-3"], '
        '"mdadm": [], "id": "master", "manufacturer": '
        '"Dell Inc.", "osrelease": "9.8", "ps": "ps '
        '-efHww", "locale_info": {"timezone": "UTC", '
        '"detectedencoding": "UTF-8", '
        '"defaultlanguage": "en_US", "defaultencoding": '
        '"UTF-8"}, "fqdn": "4181631c3821", '
        '"lsb_distrib_os": "GNU/Linux", "ip_gw": true, '
        '"ip6_interfaces": {"lo": [], "eth0": []}, '
        '"num_cpus": 8, "hwaddr_interfaces": {"lo": '
        '"00:00:00:00:00:00", "eth0": '
        '"02:42:ac:1d:00:04"}, "osfullname": "Debian", '
        '"ip4_interfaces": {"lo": ["127.0.0.1"], '
        '"eth0": ["172.29.0.4"]}, "init": "unknown", '
        '"gid": 0, "master": "master", '
        '"virtual_subtype": "Docker", "dns": {"domain": '
        '"", "sortlist": [], "nameservers": ['
        '"127.0.0.11"], "ip4_nameservers": ['
        '"127.0.0.11"], "search": [], '
        '"ip6_nameservers": [], "options": ['
        '"ndots:0"]}, "ipv6": [], "cpu_flags": ["fpu", '
        '"pts", "hwp", "hwp_notify", "hwp_act_window", '
        '"hwp_epp", "flush_l1d"], "localhost": '
        '"4181631c3821", "ipv4": ["127.0.0.1", '
        '"172.29.0.4"], "username": "root", "fqdn_ip4": '
        '["172.29.0.4"], "shell": "/bin/sh", '
        '"nodename": "4181631c3821", "saltversion": '
        '"2019.2.0", "lsb_distrib_release": "9.8", '
        '"ip6_gw": false, "server_id": 685245236, '
        '"saltpath": '
        '"/usr/lib/python2.7/dist-packages/salt", '
        '"zfs_feature_flags": false, "osmajorrelease": '
        '9, "swap_total": 7807, "os_family": "Debian", '
        '"oscodename": "stretch", "osfinger": '
        '"Debian-9", "pythonversion": [2, 7, 13, '
        '"final", 0], "lsb_distrib_description": '
        '"Debian GNU/Linux 9.8 (stretch)", '
        '"kernelversion": "#1 SMP Thu May 2 14:11:38 '
        'UTC 2019", "ip4_gw": "172.29.0.1", "num_gpus": '
        '1, "virtual": "physical", "host": '
        '"4181631c3821", "disks": [], "cpu_model": '
        '"Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz", '
        '"uuid": '
        '"4c4c4544-0053-5a10-8048-c8c04f535432", '
        '"biosreleasedate": "08/09/2018", '
        '"productname": "XPS 13 9370", "osarch": '
        '"amd64", "cpuarch": "x86_64", '
        '"lsb_distrib_codename": "stretch", '
        '"osrelease_info": [9, 8], "lsb_distrib_id": '
        '"Debian", "gpus": [{"model": "Device 5917", '
        '"vendor": "intel"}], "path": '
        '"/usr/local/bin:/usr/local/sbin:/usr/local/bin'
        ':/usr/sbin:/usr/bin:/sbin:/bin", "machine_id": '
        '"8b6f0bc66c81d2b9ef76a3fc9b52b452", '
        '"os": "Debian", "pythonexecutable": '
        '"/usr/bin/python2"}',
        pillar='{"foo": "bar", "list": ["first", "second", ' '"third"]}',
    )
    return ret


@pytest.fixture
def schedule(minion_master):
    ret = Schedule.objects.create(
        minion=minion_master,
        name="job2",
        job='{"master": {"job1": {"function": "test.ping", '
        '"name": "job1", "seconds": 3600, "enabled": '
        'false, "splay": null, "jid_include": true, '
        '"maxrunning": 1}}}',
    )


@pytest.fixture
def dummy_user():
    return User.objects.create_superuser(
        "dummy_user", "dummy_user@example.com", "dummy_userpassword"
    )


@pytest.fixture
def foo_conformity():
    return Conformity.objects.create(name="foo", function="alcali.pass_salt")


@pytest.fixture
def version_conformity():
    return Conformity.objects.create(
        name="version", function="cmd.run alcali --version"
    )


@pytest.fixture
def alcali_version_state():
    ret = SaltReturns.objects.create(
        fun="cmd.run",
        jid="20190507190955945844",
        return_field='{"oh": "no"}',
        id="master",
        success=1,
        alter_time=time.strftime("%Y-%m-%d %H:%M:%S"),
        full_ret='{"fun_args": ["alcali --version"], "return": "2019.2.2"}',
    )
    return ret


@pytest.fixture
def jobs_arguments():
    ret = SaltReturns.objects.create(
        fun="dummy.state",
        jid="20190507190955945844",
        return_field='{"oh": "no"}',
        id="master",
        success=1,
        alter_time=time.strftime("%Y-%m-%d %H:%M:%S"),
        full_ret='{"fun_args": ["foo", 1, "bar=baz"], "return": "2019.2.2"}',
    )
    return ret


@pytest.fixture
def highstate_failed():
    ret = SaltReturns.objects.create(
        fun="state.apply",
        jid="20190507190955945843",
        return_field='{"pkg_|-common_packages_'
        '|-common_packages_|-installed": {'
        '"comment": "The following packages '
        "would "
        'be installed/updated: vim", "name": '
        '"common_packages", "start_time": '
        '"19:09:59.565546", "result": null, '
        '"duration": 412.241, "__run_num__": '
        "0, "
        '"__sls__": "common.packages", '
        '"changes": '
        '{}, "__id__": "common_packages"}, '
        '"pkg_|-install_alcali_'
        "|-install_alcali_ "
        '|-installed": {"comment": "All '
        "specified "
        'packages are already installed", '
        '"name": '
        '"curl", "start_time": '
        '"19:09:59.978059", '
        '"result": true, "duration": 34.526, '
        '"__run_num__": 1, "__sls__": '
        '"alcali", '
        '"changes": {}, "__id__": '
        '"install_alcali"}}',
        id="2e220fd40bc5",
        success=1,
        full_ret='{"fun_args": ["test=True"], "jid": '
        '"20190507190955945843", "return": ["SLS Data failed to compile"], '
        '"retcode": 0, "success": false, '
        '"cmd": "_return", "_stamp": '
        '"2019-05-07T19:10:00.018461", '
        '"fun": "state.apply", "id": "master", '
        '"out": "highstate"}',
        alter_time="2019-05-07 19:10:00",
    )
    return ret
