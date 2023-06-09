from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile


# @receiver(post_save, sender=Profile)
def createprofile(sender, instance, created, **kwargs):
    print('Profile signal triggered!')
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )


def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createprofile, sender=User)
post_save.connect(update_user, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
