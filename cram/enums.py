from django.db.models import IntegerChoices


class RevisionStatus(IntegerChoices):
    AGAIN = 0, "Again"
    HARD = 1, "Hard"
    NORMAL = 2, "Normal"
    EASY = 3, "Easy"
