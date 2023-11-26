import typing as t
from uuid import UUID, uuid4

from django.db import models


QS = t.TypeVar("QS", bound="QuerySet")
M = t.TypeVar("M", bound=models.Model)
T = t.TypeVar("T")


class QuerySet(models.QuerySet[M]):
    # IMPORTANT: This QuerySet MUST NOT contain code specific to the definition
    # of 'Model' below.  It MUST be applicable to Django models that don't
    # inherit from 'kaiko.utils.db.Model'.

    model: t.Type[M]

    # fmt: off
    @t.overload
    def pks(self, *, stringify: t.Literal[True] = True) -> t.Sequence[str]:
        ...  # noqa

    @t.overload
    def pks(self, *, stringify: t.Literal[False] = False) -> t.Sequence[int | str | UUID]:
        ...  # noqa

    # fmt: on

    def pks(self, *, stringify: bool = True):
        """Return the list of stringified(or not) primary keys."""
        if stringify:
            return self.mapped(lambda instance: str(instance.pk))
        else:
            return self.mapped(lambda instance: instance.pk)

    def mapped(self, fn: t.Callable[[M], T]) -> t.Sequence[T]:
        """Performs a map from the matched objects."""
        return [fn(obj) for obj in self]


class Model(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    objects: QuerySet = QuerySet.as_manager()  # type: ignore

    class Meta:
        abstract = True


class TrackedModel(models.Model):
    """Model that tracks creation and update time."""

    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        verbose_name="Creation date",
        auto_now_add=True,
        db_index=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Last modification date",
        auto_now=True,
        db_index=True,
    )
