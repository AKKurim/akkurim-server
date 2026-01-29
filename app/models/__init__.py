from ._base_model import BaseModel
from .athlete import Athlete
from .athlete_guardian import AthleteGuardian
from .athlete_meet_event import AthleteMeetEvent
from .athlete_registration_meet_event import AthleteRegistrationMeetEvent
from .athlete_sign_up_form import AthleteSignUpForm
from .category import Category
from .club import Club
from .discipline import Discipline
from .discipline_type import DisciplineType
from .file import File
from .group import Group
from .group_athlete import GroupAthlete
from .group_trainer import GroupTrainer
from .guardian import Guardian
from .helper import Helper
from .item import Item
from .item_type import ItemType
from .meet import Meet
from .meet_event import MeetEvent
from .meet_trainer import MeetTrainer
from .payment import Payment
from .points import Points
from .remote_config import RemoteConfig
from .request import Request
from .request_file import RequestFile
from .response import Response
from .school_year import SchoolYear
from .sign_up_form import SignUpForm
from .sign_up_form_group import SignUpFormGroup
from .trainer import Trainer
from .training import Training, TrainingDashboardRead
from .training_athlete import TrainingAthlete
from .training_time import TrainingTime
from .training_trainer import TrainingTrainer
from .web_post import WebPost

__all__ = [
    "BaseModel",
    "Athlete",
    "AthleteGuardian",
    "AthleteMeetEvent",
    "AthleteRegistrationMeetEvent",
    "AthleteSignUpForm",
    "Category",
    "Club",
    "Discipline",
    "DisciplineType",
    "File",
    "Group",
    "GroupAthlete",
    "GroupTrainer",
    "Guardian",
    "Helper",
    "Item",
    "ItemType",
    "Meet",
    "MeetEvent",
    "MeetTrainer",
    "Payment",
    "Points",
    "RemoteConfig",
    "Request",
    "RequestFile",
    "Response",
    "SchoolYear",
    "SignUpForm",
    "SignUpFormGroup",
    "Trainer",
    "Training",
    "TrainingDashboardRead",
    "TrainingAthlete",
    "TrainingTime",
    "TrainingTrainer",
    "WebPost",
]

# Mapping of database table names to model classes
models_by_table_name = {
    "remote_config": RemoteConfig,
    "athlete": Athlete,
    "meet": Meet,
    "athlete_registration_meet_event": AthleteRegistrationMeetEvent,
    "response": Response,
    "athlete_meet_event": AthleteMeetEvent,
    "payment": Payment,
    "web_post": WebPost,
    "meet_event": MeetEvent,
    "meet_trainer": MeetTrainer,
    "trainer": Trainer,
    "training_athlete": TrainingAthlete,
    "discipline_type": DisciplineType,
    "discipline": Discipline,
    "group_trainer": GroupTrainer,
    "helper": Helper,
    "sign_up_form_group": SignUpFormGroup,
    "category": Category,
    "school_year": SchoolYear,
    "request_file": RequestFile,
    "request": Request,
    "athlete_guardian": AthleteGuardian,
    "group_athlete": GroupAthlete,
    "training_trainer": TrainingTrainer,
    "guardian": Guardian,
    "points": Points,
    "training": Training,
    "club": Club,
    "group": Group,
    "item": Item,
    "sign_up_form": SignUpForm,
    "athlete_sign_up_form": AthleteSignUpForm,
    "training_time": TrainingTime,
    "file": File,
    "item_type": ItemType,
}
