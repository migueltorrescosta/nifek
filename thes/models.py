from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    DateTimeField,
    TextField,
    CASCADE,
    PROTECT,
)
from django.contrib.auth.models import User


class Thesis(Model):

    author = ForeignKey(User, on_delete=PROTECT, related_name="theses")
    content = TextField()
    updated_on = DateTimeField(auto_now=True, null=False)
    created_on = DateTimeField(auto_now_add=True, null=False)

    class Meta:
        ordering = ["-created_on"]
        verbose_name_plural = "theses"

    def __str__(self):
        return f"'{self.content}'- by {self.author}"


class Property(Model):

    author = ForeignKey(User, on_delete=PROTECT, related_name="properties")
    text = CharField(max_length=20, null=False)
    updated_on = DateTimeField(auto_now=True, null=False)
    created_on = DateTimeField(auto_now_add=True, null=False)

    class Meta:
        ordering = ["-created_on"]
        verbose_name_plural = "properties"

    def __str__(self):
        return str(self.text)


class Tag(Model):
    # A note corresponds to a tag submitted by a user on a thesis
    tagger = ForeignKey(User, on_delete=PROTECT, related_name="tags")
    thesis = ForeignKey(Thesis, on_delete=PROTECT, related_name="tags")
    property = ForeignKey(Property, on_delete=PROTECT, related_name="tags")
    updated_on = DateTimeField(auto_now=True, null=False)
    created_on = DateTimeField(auto_now_add=True, null=False)
    deleted_on = DateTimeField(default=None, null=True, blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.tagger} applied tag {self.property} to thesis #{self.thesis.id}"
