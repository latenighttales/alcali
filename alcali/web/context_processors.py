from alcali.web.models.alcali import Notifications


def notifications(request):
    if request.user.is_authenticated:
        notifs_list = []
        notifs = Notifications.objects.all()
        for notif in notifs:
            notif_data = {
                "notif_attr": notif.notif_attr(),
                "id": notif.id,
                "datetime": notif.datetime(),
            }
            notifs_list.append(notif_data)
        return {"notifs_list": notifs_list}
    return {}
