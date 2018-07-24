from peasantlegaldb import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=models.Litigant)
def update_litigant_dates_on_save(sender, instance, **kwargs):
    # check to see if the litigant has an earliest and latest case, if not, assign this case to those fields, if so
    # compare and assign accordingly.
    if not instance.person.earliest_case:
        instance.person.earliest_case = instance.case
    elif instance.person.earliest_case.session.date > instance.case.session.date:
        instance.person.earliest_case = instance.case
    if not instance.person.latest_case:
        instance.person.latest_case = instance.case
    elif instance.person.latest_case.session.date < instance.case.session.date:
        instance.person.latest_case = instance.case
    instance.person.save(update_fields=['earliest_case', 'latest_case'])
    # check if the litigant is tied to any lands. If so, update their respective earliest and latest cases.
    if instance.lands:
        for land in instance.lands.all():
            if not land.land.earliest_case:
                land.land.earliest_case = instance.case
            elif land.land.earliest_case.session.date > instance.case.session.date:
                land.land.earliest_case = instance.case
            if not land.land.latest_case:
                land.land.latest_case = instance.case
            elif land.land.latest_case.session.date < instance.case.session.date:
                land.land.latest_case = instance.case
            land.land.save(update_fields=['earliest_case', 'latest_case'])


@receiver(post_delete, sender=models.Litigant)
def update_litigant_dates_on_delete(sender, instance, **kwargs):
    if instance.person.earliest_case == instance.case or instance.person.latest_case == instance.case:
        if instance.person.earliest_case == instance.case:
            try:
                instance.person.earliest_case = models.Case.objects.filter(litigants__person=instance.person).\
                    earliest('session__date')
            except models.Case.DoesNotExist:
                instance.person.earliest_case = None
        if instance.person.latest_case == instance.case:
            try:
                instance.person.latest_case = models.Case.objects.filter(litigants__person=instance.person).\
                    latest('session__date')
            except models.Case.DoesNotExist:
                instance.person.latest_case = None
        instance.person.save(update_fields=['earliest_case', 'latest_case'])
    if instance.lands:
        for land in instance.lands.all():
            if land.land.earliest_case == instance.case or land.land.latest_case == instance.case:
                if land.land.earliest_case == instance.case:
                    try:
                        land.land.earliest_case = models.Case.objects.filter(litigants__lands__land=land).\
                            earliest('session__date')
                    except models.Case.DoesNotExist:
                        land.land.earliest_case = None
                if land.land.latest_case == instance.case:
                    try:
                        land.land.latest_case = models.Case.objects.filter(litigants__lands__land=land).\
                            latest('session__date')
                    except models.Case.DoesNotExist:
                        land.land.latest_case = None
                land.land.save(update_fields=['earliest_case', 'latest_case'])


@receiver(post_save, sender=models.Pledge)
def update_pledge_giver_dates_on_save(sender, instance, **kwargs):
    if not instance.giver.earliest_case:
        instance.giver.earliest_case = instance.receiver.case
    elif instance.giver.earliest_case.session.date > instance.receiver.case.session.date:
        instance.giver.earliest_case = instance.receiver.case
    if not instance.giver.latest_case:
        instance.giver.latest_case = instance.receiver.case
    elif instance.giver.latest_case.session.date < instance.receiver.case.session.date:
        instance.giver.latest_case = instance.receiver.case
    instance.giver.save(update_fields=['earliest_case', 'latest_case'])


@receiver(post_delete, sender=models.Pledge)
def update_pledge_giver_dates_on_delete(sender, instance, **kwargs):
    if instance.giver.earliest_case == instance.receiver.case or instance.giver.latest_case == instance.receiver.case:
        if instance.giver.earliest_case == instance.receiver.case:
            try:
                instance.giver.earliest_case = models.Case.objects.filter(litigants__person=instance.giver).\
                    earliest('session__date')
            except models.Case.DoesNotExist:
                instance.giver.earliest_case = None
        if instance.giver.latest_case == instance.receiver.case:
            try:
                instance.giver.latest_case = models.Case.objects.filter(litigants__person=instance.giver).\
                    latest('session__date')
            except models.Case.DoesNotExist:
                instance.giver.latest_case = None
        instance.giver.save(update_fields=['earliest_case', 'latest_case'])