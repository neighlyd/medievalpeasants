from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from peasantlegaldb.models import Archive, Case, Person, Record, Village


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)


class Project(models.Model):
    researcher = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    description = models.TextField()
    archives = models.ManyToManyField(Archive)
    cases = models.ManyToManyField(Case)
    people = models.ManyToManyField(Person)
    records = models.ManyToManyField(Record)
    villages = models.ManyToManyField(Village)

    def __str__(self):
        return '{}'.format(self.title)