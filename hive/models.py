from djangoldp.models import Model
from django.db import models
from content.models import Tag, NameContent


class Hive(Model):
    """A collection of actors belonging to a single consciousness e.g. the player"""
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def size(self):
        return self.actors.count()

    def __str__(self):
        return self.name


class Group(Model):
    """An abstract form of grouping, to represent membership"""
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Actor(Model):
    """A member, or potential member of a hive"""
    hive = models.ForeignKey(Hive, on_delete=models.SET_NULL, related_name='actors', null=True, default=None)
    name = models.ForeignKey(NameContent, on_delete=models.SET_NULL, related_name='actors', null=True)
    age = models.PositiveIntegerField(null=False, default=18)

    def __str__(self):
        return str(self.name) + " (" + str(self.hive) + ")"


class GroupMember(Model):
    """A many to many between Groups and Actors"""
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='groups')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='actors')


class ActorTag(Model):
    """A many to many between Tags and Actors"""
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='actors')
