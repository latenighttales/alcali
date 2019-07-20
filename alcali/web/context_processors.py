from alcali.web.models.alcali import Notifications


def notifications(request):
    if request.user.is_authenticated:
        notifs_list = []
        notifs = Notifications.objects.all()
        for notif in notifs:
            notifs_list.append(
                {
                    "notif_attr": notif.notif_attr(),
                    "id": notif.id,
                    "datetime": notif.datetime(),
                }
            )
        return {"notifs_list": notifs_list}
    return {}
