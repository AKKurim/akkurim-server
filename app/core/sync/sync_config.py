from app.core.remote_config.schemas import ClubReadPublic, RemoteConfigReadPublic
from app.core.shared.join_tables import (
    AthleteGuardainReadPublic,
    AthleteMeetEventReadPublic,
    AthleteSignUpFormReadPublic,
    GroupAthleteReadPublic,
    GroupTrainerReadPublic,
    TrainingAthleteReadPublic,
    TrainingTrainerReadPublic,
)
from app.core.shared.schemas import SchoolYearReadPublic
from app.features.athlete.schemas import AthleteReadPublic, SignUpFormReadPublic
from app.features.attendance.schemas import (
    GroupReadPublic,
    TrainingReadPublic,
    TrainingTimeReadPublic,
)
from app.features.guardian.schemas import GuardianReadPublic
from app.features.item.schemas import ItemReadPublic, ItemTypeReadPublic
from app.features.meet.schemas import (
    CategoryReadPublic,
    DisciplineReadPublic,
    DisciplineTypeReadPublic,
    MeetEventReadPublic,
    MeetReadPublic,
)
from app.features.trainer.schemas import TrainerReadPublic
from app.features.web_management.schemas import WebPostReadPublic

# TODO edit this file to use the new schemas
TABLE_NAMES = {
    # "table_name": Schema
    "club": ClubReadPublic,
    "remote_config": RemoteConfigReadPublic,
    "school_year": SchoolYearReadPublic,
    "athlete": AthleteReadPublic,
    "trainer": TrainerReadPublic,
    "guardian": GuardianReadPublic,
    "athlete_guardian": AthleteGuardainReadPublic,
    "item": ItemReadPublic,
    "item_type": ItemTypeReadPublic,
    "web_post": WebPostReadPublic,
    "group": GroupReadPublic,
    "group_athlete": GroupAthleteReadPublic,
    "group_trainer": GroupTrainerReadPublic,
    "training": TrainingReadPublic,
    "training_time": TrainingTimeReadPublic,
    "training_athlete": TrainingAthleteReadPublic,
    "training_trainer": TrainingTrainerReadPublic,
    "sign_up_form": SignUpFormReadPublic,
    "meet": MeetReadPublic,
    "discipline": DisciplineReadPublic,
    "discipline_type": DisciplineTypeReadPublic,
    "category": CategoryReadPublic,
    "meet_event": MeetEventReadPublic,
    "athlete_meet_event": AthleteMeetEventReadPublic,
    "athlete_sign_up_form": AthleteSignUpFormReadPublic,
}
