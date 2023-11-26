import typing as t
from django.db import models
from pyrightbug6542.utils import db

MAX_ATTACHMENT_NAME_LENGTH = 1024


class TombstoneQS(db.QuerySet["Tombstone"]):
    def dispose(self, *, batch_size: int = 200):
        ...


class Tombstone(db.TrackedModel, db.Model):
    filename = models.CharField(max_length=MAX_ATTACHMENT_NAME_LENGTH)
    objects: t.ClassVar[TombstoneQS] = TombstoneQS.as_manager()  # type: ignore


def dispose_tombstones(limit: int = 500):
    tombstones = Tombstone.objects.all()[:limit]
    tombstones.dispose()
