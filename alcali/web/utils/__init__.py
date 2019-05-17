import json
from collections import Counter
from difflib import SequenceMatcher
from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.db.models import Count, Q

from ..models.salt import SaltReturns
from ..models.alcali import Minions, Conformity


def auto_group(minion_list):
    return SequenceMatcher(None, [i for i in minion_list]).find_longest_match([0, ])


# Find all occurrences of a key in nested python dictionaries and lists.
def find_key(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find_key(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find_key(key, d):
                    yield result


def graph_data(period=7, **kwargs):
    """
    Retrieve graph data, count nb of jobs per days.
    :param period: nb of days
    :return: (days, count): list of days, nb of jobs.
    """
    period_frame = timezone.now().date() - timedelta(days=period)

    if kwargs.get('fun') == 'highstate':
        kwargs.pop('fun')
        data = SaltReturns.objects.filter(
            Q(fun='state.apply') | Q(fun='state.highstate'),
            alter_time__gt=period_frame, **kwargs).extra(
            {"day": "date(alter_time)"}).values('day').annotate(
            count=Count('jid')).annotate(
            error=Count('success', filter=Q(success='0'))).order_by('day')

    elif kwargs.get('fun') == 'other':
        kwargs.pop('fun')
        data = SaltReturns.objects.filter(
            alter_time__gt=period_frame, **kwargs).exclude(
            Q(fun='state.apply') | Q(fun='state.highstate')).extra(
            {"day": "date(alter_time)"}).values('day').annotate(
            count=Count('jid')).annotate(
            error=Count('success', filter=Q(success='0'))).order_by('day')

    else:
        kwargs.pop('fun')
        data = SaltReturns.objects.filter(
            alter_time__gt=period_frame, **kwargs).extra(
            {"day": "date(alter_time)"}).values('day').annotate(
            count=Count('jid')).annotate(
            error=Count('success', filter=Q(success='0'))).order_by('day')

    days = []
    count = []
    error_count = []
    for res in data:
        days.append(str(res['day']))
        count.append(res['count'])
        error_count.append(res['error'])
    for idx, date in enumerate(period_frame + timedelta(n) for n in range(period)):
        if str(date) not in days:
            days.insert(idx, str(date))
            count.insert(idx, 0)
            error_count.insert(idx, 0)

    return days, count, error_count


def render_conformity():
    minions_all = Minions.objects.all()
    conformity_fields = Conformity.objects.values('name', 'function')
    if not conformity_fields:
        return [], []
    conformity_names = [i['name'].upper() for i in conformity_fields]
    ret = []
    for field in conformity_fields:
        field_ret = []
        args = field['function'].split(' ')
        kwargs = {}
        for arg in args:
            if '=' in arg:
                kwargs[arg.split('=')[0]] = arg.split('=')[1]
                args.remove(arg)

        for minion in minions_all:
            conformity_field = minion.custom_conformity(*args, **kwargs)
            if isinstance(conformity_field, dict):
                field_ret.append(list(conformity_field.values())[0])
            else:
                field_ret.append(conformity_field)
        ret.append(dict(Counter(field_ret)))

    return conformity_names, ret


def check_permission(function):
    """
    Check if user has permission, from Salt-api login return.

    :param function:
    :return:
    """

    def _function(request, *args, **kwargs):
        perms = json.loads(request.user.user_settings.salt_permissions)
        if not any(function.__name__ in perm for perm in perms):
            raise PermissionDenied
        return function(request, *args, **kwargs)

    return _function
