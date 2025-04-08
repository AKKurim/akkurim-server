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
from app.features.athlete.schemas import (
    AthleteReadPublic,
    AthleteStatusReadPublic,
    SignUpFormReadPublic,
    SignUpFormStatusReadPublic,
)
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
from app.features.trainer.schemas import TrainerReadPublic, TrainerStatusReadPublic
from app.features.web_management.schemas import WebPostReadPublic

TABLE_NAMES = {
    # "table_name": Schema
    "club": ClubReadPublic,
    "remote_config": RemoteConfigReadPublic,
    "school_year": SchoolYearReadPublic,
    "athlete": AthleteReadPublic,
    "athlete_status": AthleteStatusReadPublic,
    "trainer": TrainerReadPublic,
    "trainer_status": TrainerStatusReadPublic,
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
    "sign_up_form_status": SignUpFormStatusReadPublic,
    "meet": MeetReadPublic,
    "discipline": DisciplineReadPublic,
    "discipline_type": DisciplineTypeReadPublic,
    "category": CategoryReadPublic,
    "meet_event": MeetEventReadPublic,
    "athlete_meet_event": AthleteMeetEventReadPublic,
    "athlete_sign_up_form": AthleteSignUpFormReadPublic,
}
