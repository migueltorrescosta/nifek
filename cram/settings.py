from datetime import timedelta
from collections import defaultdict
from enums import RevisionStatus

MINIMUM_TIME_INTERVAL: defaultdict[int, timedelta] = defaultdict(
    lambda: timedelta(minutes=5)
)
MINIMUM_TIME_INTERVAL[RevisionStatus.HARD] = timedelta(minutes=30)
MINIMUM_TIME_INTERVAL[RevisionStatus.NORMAL] = timedelta(hours=12)
MINIMUM_TIME_INTERVAL[RevisionStatus.EASY] = timedelta(hours=48)
