from collections import defaultdict
from datetime import timedelta

from .enums import RevisionStatus

MINIMUM_TIME_INTERVAL = defaultdict(lambda: timedelta(minutes=2))
MINIMUM_TIME_INTERVAL[RevisionStatus.HARD] = timedelta(minutes=60)
MINIMUM_TIME_INTERVAL[RevisionStatus.NORMAL] = timedelta(hours=12)
MINIMUM_TIME_INTERVAL[RevisionStatus.EASY] = timedelta(hours=48)
RANDOMNESS_RANGE = 0.5

MAXIMUM_UNKNOWN_CARDS = 3
