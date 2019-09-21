from collections import Counter

# from difflib import SequenceMatcher
from datetime import timedelta

from django.utils import timezone
from django.db.models import Count, Q

from .input import RawCommand
from ..models import SaltReturns
from ..models import Minions, Conformity


# def auto_group(minion_list):
#     return SequenceMatcher(None, [i for i in minion_list]).find_longest_match([0])
#

# Find all occurrences of a key in nested python dictionaries and lists.
# def find_key(key, dictionary):
#     for k, v in dictionary.items():
#         if k == key:
#             yield v
#         elif isinstance(v, dict):
#             for result in find_key(key, v):
#                 yield result
#         elif isinstance(v, list):
#             for d in v:
#                 for result in find_key(key, d):
#                     yield result
#


def graph_data(period=7, **kwargs):
    """
    Retrieve graph data, count nb of jobs per days.
    :param period: nb of days
    :return: (days, count): list of days, nb of jobs.
    """
    period_frame = timezone.now().date() - timedelta(days=period)

    if kwargs.get("fun") == "highstate":
        kwargs.pop("fun")
        data = (
            SaltReturns.objects.filter(
                Q(fun="state.apply") | Q(fun="state.highstate"),
                alter_time__gt=period_frame,
                **kwargs
            )
            .extra({"day": "date(alter_time)"})
            .values("day")
            .annotate(count=Count("jid"))
            .annotate(error=Count("success", filter=Q(success="0")))
            .order_by("day")
        )

    elif kwargs.get("fun") == "other":
        kwargs.pop("fun")
        data = (
            SaltReturns.objects.filter(alter_time__gt=period_frame, **kwargs)
            .exclude(Q(fun="state.apply") | Q(fun="state.highstate"))
            .extra({"day": "date(alter_time)"})
            .values("day")
            .annotate(count=Count("jid"))
            .annotate(error=Count("success", filter=Q(success="0")))
            .order_by("day")
        )

    else:
        kwargs.pop("fun")
        data = (
            SaltReturns.objects.filter(alter_time__gt=period_frame, **kwargs)
            .extra({"day": "date(alter_time)"})
            .values("day")
            .annotate(count=Count("jid"))
            .annotate(error=Count("success", filter=Q(success="0")))
            .order_by("day")
        )

    days = []
    count = []
    error_count = []
    for res in data:
        days.append(str(res["day"]))
        count.append(res["count"])
        error_count.append(res["error"])
    for idx, date in enumerate(period_frame + timedelta(n) for n in range(period)):
        # Complete all lists with default data.
        if str(date) not in days:
            days.insert(idx, str(date))
            count.insert(idx, 0)
            error_count.insert(idx, 0)

    return days, count, error_count


def render_conformity(target=None):

    # First, a list of targets.
    if target:
        minions_all = [Minions.objects.get(minion_id=target)]
    else:
        minions_all = Minions.objects.all()

    # Get conformity fields.
    conformity_fields = Conformity.objects.values("name", "function")

    # Default.
    if not conformity_fields:
        return [], [], []

    # Create list of conformity names in UPPERCASE.
    conformity_names = [i["name"].upper() for i in conformity_fields]

    # Aggregated results structure.
    ret = []

    # Detailed structure.
    details = {minion.minion_id: [] for minion in minions_all}

    for field in conformity_fields:
        field_ret = []

        # Parse command.
        funct = field["function"]
        # Use fake client because we don't provide a target
        parser = RawCommand(funct, client="runner", inline=True)
        parsed = parser.parse()[0]

        for minion in minions_all:
            if "arg" in parsed:
                conformity_field = minion.custom_conformity(
                    parsed["fun"], *parsed["arg"]
                )
            else:
                conformity_field = minion.custom_conformity(parsed["fun"])

            # If the job return is a dict, get the value.
            if isinstance(conformity_field, dict):
                conformity_ret = list(conformity_field.values())[0]
                field_ret.append(conformity_ret)
                details[minion.minion_id].append({field["name"]: conformity_ret})
            # It should be a string.
            else:
                field_ret.append(conformity_field)
                details[minion.minion_id].append({field["name"]: conformity_field})
        ret.append(dict(Counter(field_ret)))

    return conformity_names, ret, details
