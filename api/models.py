# https://github.com/beda-software/drf-writable-nested/blob/master/tests/models.py

import uuid
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Site(models.Model):
    url = models.CharField(max_length=100)


class User(models.Model):
    username = models.CharField(max_length=100)
    user_avatar = models.ForeignKey(
        'Avatar',
        null=True,
        on_delete=models.PROTECT
    )


class AccessKey(models.Model):
    key = models.CharField(max_length=100)


class Profile(models.Model):
    sites = models.ManyToManyField(Site)
    user = models.OneToOneField(User)
    access_key = models.ForeignKey(AccessKey, null=True)


class Avatar(models.Model):
    image = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, related_name='avatars',)


class Tag(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class TaggedItem(models.Model):
    tags = GenericRelation(Tag)


class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)


class CustomPK(models.Model):
    slug = models.SlugField(
        primary_key=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='custompks',
    )


class Message(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    profile = models.ForeignKey(Profile, related_name='messages')
    message = models.CharField(max_length=100)
