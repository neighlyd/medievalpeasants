from peasantlegaldb import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=models.Litigant)
def update_litigant_dates_on_save(sender, instance, **kwargs):

    def update_old_litigant_case_dates(obj, instance):
        # check to see if the old litigant's earliest or latest case was this one. If so, check to see if they have
        # any other cases that are earlier or later. If they do, assign to appropriate field and save.
        if obj.earliest_case == instance.case or obj.latest_case == instance.case:
            if obj.earliest_case == instance.case:
                # Because a person can be involved in cases as either a Litigant or a Pledge, search for both and sort.
                earliest_case_list = []
                try:
                    earliest_case_list.append(models.Case.objects.filter(litigants__person=row).earliest('case__session__date'))
                except models.Case.DoesNotExist:
                    pass
                try:
                    earliest_case_list.append(models.Case.objects.filter(litigants__pledges__giver=row).earliest('receiver__case__session_date'))
                except models.Case.DoesNotExist:
                    pass
                if not earliest_case_list:
                    obj.earliest_case = None
                else:
                    obj.earliest_case = sorted(earliest_case_list, key=lambda x: x.session.date)[0]

            if obj.latest_case == instance.case:
                latest_case_list = []
                try:
                    latest_case_list.append(models.Case.objects.filter(litigants__person=row).latest('session__date'))
                except models.Case.DoesNotExist:
                    pass
                try:
                    latest_case_list.append(models.Case.objects.filter(litigants__pledges__giver=row).latest('session_date'))
                except models.Case.DoesNotExist:
                    pass
                if not latest_case_list:
                    obj.latest_case = None
                else:
                    obj.latest_case = sorted(latest_case_list, key=lambda x: x.session.date, reverse=True)[0]

            obj.save(update_fields=['earliest_case', 'latest_case'])

    def update_new_litigant_case_dates(instance):
            # See if litigant has an earliest or latest case. If they don't assign this case.
            # If they do, compare dates and assign accordingly.
            # There is no need to check the pledge dates, since we are only comparing to this case and not clearing out
            # and updating the field.
            if not instance.person.earliest_case:
                instance.person.earliest_case = instance.case
            elif instance.person.earliest_case.session.date > instance.case.session.date:
                instance.person.earliest_case = instance.case
            if not instance.person.latest_case:
                instance.person.latest_case = instance.case
            elif instance.person.latest_case.session.date < instance.case.session.date:
                instance.person.latest_case = instance.case
            instance.person.save(update_fields=['earliest_case', 'latest_case'])

    def update_land_dates(instance):
        # Check if there are lands associated with case. If so, iterate through them and adjust their dates accordingly.
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

    # see if there was a previous Person (i.e. is this an update to the person field or a new entry).
    # Otherwise, only update the person saved in Litigant model.
    if instance.tracker.has_changed('person'):
        previous_litigant = models.Person.objects.get(id=instance.tracker.previous('person'))
        # need to send both the previous_litigant instance (a person model instance) and the instance variable, as the
        # instance refers to the litigant instance itself, which is where we get the current case information.
        update_old_litigant_case_dates(previous_litigant, instance)
        update_new_litigant_case_dates(instance)
        update_land_dates(instance)
    else:
        update_new_litigant_case_dates(instance)
        update_land_dates(instance)


@receiver(post_delete, sender=models.Litigant)
def update_litigant_dates_on_delete(sender, instance, **kwargs):
    if instance.person.earliest_case == instance.case or instance.person.latest_case == instance.case:
        # get dates for cases where person is both a Litigant and a Pledge and compare those dates.
        if instance.person.earliest_case == instance.case:
            try:
                as_litigant = models.Case.objects\
                    .prefetch_related('litigants')\
                    .select_related('session')\
                    .filter(litigants__person=instance.person)\
                    .earliest('session__date')
            except models.Case.DoesNotExist:
                as_litigant = None
            try:
                as_pledge = models.Case.objects\
                        .select_related('session')\
                        .prefetch_related('litigants__pledges')\
                        .filter(litigants__pledges__giver=instance.person)\
                        .earliest('session__date')
            except models.Case.DoesNotExist:
                as_pledge = None
            if as_litigant is not None and as_pledge is not None:
                if as_litigant.session.date < as_pledge.session.date:
                    instance.person.earliest_case = as_litigant
                else:
                    instance.person.earliest_case = as_pledge
            elif as_litigant:
                instance.person.earliest_case = as_litigant
            elif as_pledge:
                instance.person.earliest_case = as_pledge
            else:
                instance.person.earliest_case = None

        if instance.person.latest_case == instance.case:
            try:
                as_litigant = models.Case.objects\
                    .prefetch_related('litigants')\
                    .select_related('session')\
                    .filter(litigants__person=instance.person)\
                    .latest('session__date')
            except models.Case.DoesNotExist:
                as_litigant = None
            try:
                as_pledge = models.Case.objects\
                        .select_related('session')\
                        .prefetch_related('litigants__pledges')\
                        .filter(litigants__pledges__giver=instance.person)\
                        .latest('session__date')
            except models.Case.DoesNotExist:
                as_pledge = None
            if as_litigant is not None and as_pledge is not None:
                if as_litigant.session.date < as_pledge.session.date:
                    instance.person.latest_case = as_litigant
                else:
                    instance.person.latest_case = as_pledge
            elif as_litigant:
                instance.person.latest_case = as_litigant
            elif as_pledge:
                instance.person.latest_case = as_pledge
            else:
                instance.person.latest_case = None
        instance.person.save(update_fields=['earliest_case', 'latest_case'])

    if instance.lands:
        for land in instance.lands.all():
            if land.land.earliest_case == instance.case or land.land.latest_case == instance.case:
                if land.land.earliest_case == instance.case:
                    try:
                        land.land.earliest_case = models.Case.objects\
                            .prefetch_related('litigants__lands__land')\
                            .select_related('session')\
                            .filter(litigants__lands__land=land)\
                            .earliest('session__date')
                    except models.Case.DoesNotExist:
                        land.land.earliest_case = None
                if land.land.latest_case == instance.case:
                    try:
                        land.land.latest_case = models.Case.objects\
                            .prefetch_related('litigants__lands__land')\
                            .select_related('session')\
                            .filter(litigants__lands__land=land)\
                            .latest('session__date')
                    except models.Case.DoesNotExist:
                        land.land.latest_case = None
                land.land.save(update_fields=['earliest_case', 'latest_case'])


@receiver(post_save, sender=models.Pledge)
def update_pledger_dates_on_save(sender, instance, **kwargs):
    # only need to update the giver, as the receiver's case dates are covered by the update_lit_dates_on_save method.
    def update_old_pledge_giver(obj, instance):
        if obj.earliest_case == instance.receiver.case or obj.latest_case == instance.receiver.case:
            if obj.earliest_case == instance.receiver.case:
                try:
                    as_litigant = models.Case.objects\
                        .prefetch_related('litigants')\
                        .select_related('session')\
                        .filter(litigants__person=obj)\
                        .earliest('session__date')
                except models.Case.DoesNotExist:
                    as_litigant = None
                try:
                    as_pledge = models.Case.objects\
                        .select_related('session')\
                        .prefetch_related('litigants__pledges')\
                        .filter(litigants__pledges__giver=obj)\
                        .earliest('session__date')
                except models.Case.DoesNotExist:
                    as_pledge = None

                if as_litigant is not None and as_pledge is not None:
                    if as_litigant.session.date < as_pledge.session.date:
                        obj.earliest_case = as_litigant
                    else:
                        obj.earliest_case = as_pledge
                elif as_litigant is not None:
                    obj.earliest_case = as_litigant
                elif as_pledge is not None:
                    obj.earliest_case = as_pledge
                else:
                    obj.earliest_case = None

            if obj.latest_case == instance.receiver.case:
                try:
                    as_litigant = models.Case.objects\
                        .select_related('session')\
                        .prefetch_related('litigants')\
                        .filter(litigants__person=obj)\
                        .latest('session__date')
                except models.Case.DoesNotExist:
                    as_litigant = None
                try:
                    as_pledge = models.Case.objects \
                        .select_related('session') \
                        .prefetch_related('litigants__pledges') \
                        .filter(litigants__pledges__giver=obj) \
                        .latest('session__date')
                except models.Case.DoesNotExist:
                    as_pledge = None

                if as_litigant is not None and as_pledge is not None:
                    if as_litigant.session.date > as_pledge.session.date:
                        obj.latest_case = as_litigant
                    else:
                        obj.latest_case = as_pledge
                elif as_litigant:
                    obj.latest_case = as_litigant
                elif as_pledge:
                    obj.latest_case = as_pledge
                else:
                    obj.latest_case = None
        obj.save(update_fields=['earliest_case', 'latest_case'])

    def update_new_pledge_giver(instance):
        if not instance.giver.earliest_case:
            instance.giver.earliest_case = instance.receiver.case
        elif instance.giver.earliest_case.session.date > instance.receiver.case.session.date:
            instance.giver.earliest_case = instance.receiver.case
        if not instance.giver.latest_case:
            instance.giver.latest_case = instance.receiver.case
        elif instance.giver.latest_case.session.date < instance.receiver.case.session.date:
            instance.giver.latest_case = instance.receiver.case
        instance.giver.save(update_fields=['earliest_case', 'latest_case'])

    if instance.tracker.has_changed('giver'):
        previous_giver = models.Person.objects.get(id=instance.tracker.previous('giver'))
        update_old_pledge_giver(previous_giver, instance)
        update_new_pledge_giver(instance)
    else:
        update_new_pledge_giver(instance)




@receiver(post_delete, sender=models.Pledge)
def update_pledge_giver_dates_on_delete(sender, instance, **kwargs):
    if instance.giver.earliest_case == instance.receiver.case or instance.person.latest_case == instance.receiver.case:
        # get dates for cases where person is both a Litigant and a Pledge and compare those dates.
        if instance.giver.earliest_case == instance.receiver.case:
            try:
                as_litigant = models.Case.objects\
                    .prefetch_related('litigants')\
                    .select_related('session')\
                    .filter(litigants__person=instance.giver)\
                    .earliest('session__date')
            except models.Case.DoesNotExist:
                as_litigant = None
            try:
                as_pledge = models.Case.objects\
                        .select_related('session')\
                        .prefetch_related('litigants__pledges')\
                        .filter(litigants__pledges__giver=instance.giver)\
                        .earliest('session__date')
            except models.Case.DoesNotExist:
                as_pledge = None
            if as_litigant is not None and as_pledge is not None:
                if as_litigant.session.date < as_pledge.session.date:
                    instance.giver.earliest_case = as_litigant
                else:
                    instance.giver.earliest_case = as_pledge
            elif as_litigant:
                instance.giver.earliest_case = as_litigant
            elif as_pledge:
                instance.giver.earliest_case = as_pledge
            else:
                instance.giver.earliest_case = None

        if instance.giver.latest_case == instance.receiver.case:
            try:
                as_litigant = models.Case.objects\
                    .prefetch_related('litigants')\
                    .select_related('session')\
                    .filter(litigants__person=instance.giver)\
                    .latest('session__date')
            except models.Case.DoesNotExist:
                as_litigant = None
            try:
                as_pledge = models.Case.objects\
                        .select_related('session')\
                        .prefetch_related('litigants__pledges')\
                        .filter(litigants__pledges__giver=instance.giver)\
                        .latest('session__date')
            except models.Case.DoesNotExist:
                as_pledge = None
            if as_litigant is not None and as_pledge is not None:
                if as_litigant.session.date < as_pledge.session.date:
                    instance.giver.latest_case = as_litigant
                else:
                    instance.giver.latest_case = as_pledge
            elif as_litigant:
                instance.giver.latest_case = as_litigant
            elif as_pledge:
                instance.giver.latest_case = as_pledge
            else:
                instance.giver.latest_case = None
        instance.giver.save(update_fields=['earliest_case', 'latest_case'])