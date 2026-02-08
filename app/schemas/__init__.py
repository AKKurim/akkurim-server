from .attendance import (
    AthleteAttendanceItem,
    TrainerAttendanceItem,
    TrainingAttendanceDetail,
)
from .group import GroupCreateUpdate, GroupReadDetail, PersonSimple
from .training import TrainingDashboardRead

__all__ = [
    "TrainingDashboardRead",
    "AthleteAttendanceItem",
    "TrainerAttendanceItem",
    "TrainingAttendanceDetail",
    "GroupCreateUpdate",
    "GroupReadDetail",
    "PersonSimple",
]
