import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action


def create_action(user, verb, target=None):
    #проверка на какое-л подобное действие
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id, verb=verb,
                                            created__get=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id)

    if not similar_actions:
        #если нет таких действий
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
