# from datetime import datetime
#
# import salt.config
# from salt.client import LocalClient
# from salt.exceptions import SaltReqTimeoutError
# from salt.runner import RunnerClient
# from salt.wheel import WheelClient
#
# from alcali.web.models.alcali import Minions
#
# master_conf = '/home/matt/perso/alcali/alcali/tests/conf/etc/salt/master'
# opts = salt.config.master_config(master_conf)
#
#
# def get_jobs(refresh=False):
#     if refresh:
#         try:
#             runner = RunnerClient(opts)
#             api_ret = runner.cmd(fun='jobs.list_jobs')
#             for job, value in api_ret.items():
#                 value['StartTime'] = datetime.strptime(value['StartTime'],
#                                                        '%Y, %b %d %H:%M:%S.%f')
#                 Jobs.objects.update_or_create(job_id=job,
#                                               defaults={k.lower().replace('-', '_'): v
#                                                         for k, v in value.items()})
#         except SaltReqTimeoutError:
#             print('totootot')
#     ret = Jobs.objects.all().values()
#
#     return ret
#
#
# def get_job_detail(jid):
#     runner = RunnerClient(opts)
#     ret = runner.cmd(fun='jobs.print_job', arg=[jid])
#     return ret
#
#
# def get_keys(refresh=False):
#     if refresh:
#         try:
#             wheel = WheelClient(opts)
#             ret = wheel.cmd(fun='key.list_all')
#             for minion in ret['minions']:
#                 finger = wheel.cmd(fun='key.finger', arg=[minion])
#                 finger = finger['minions'][minion]
#                 Minions.objects.update_or_create(minion_id=minion,
#                                                  defaults={'key_status': 'accepted',
#                                                         'key_finger': finger})
#         except SaltReqTimeoutError:
#             print("Connection failed!!!\n\n")
#             pass
#     ret = Minions.objects.all().values()
#
#     return ret
#
#
# def get_grains(minion_id):
#     local = LocalClient(c_path=master_conf)
#     ret = local.cmd(minion_id, 'grains.items')
#     return ret
#
#
# def run_job(tgt, fun, args, kwargs=None):
#     local = LocalClient(c_path=master_conf)
#     ret = local.cmd(tgt,
#                     fun,
#                     args,
#                     kwarg=kwargs
#                     )
#     return ret
