from app.core.files.schemas import FileReadPublic
from app.core.remote_config.schemas import ClubReadPublic, RemoteConfigReadPublic
from app.core.shared.join_tables import (
    AthleteGuardainReadPublic,
    AthleteMeetEventReadPublic,
    AthleteRegistrationMeetEventReadPublic,
    AthleteSignUpFormReadPublic,
    GroupAthleteReadPublic,
    GroupTrainerReadPublic,
    RequestFileReadPublic,
    SignUpFormGroupReadPublic,
    TrainingAthleteReadPublic,
    TrainingTrainerReadPublic,
)
from app.core.shared.schemas import SchoolYearReadPublic
from app.features.athlete.schemas import (
    AthleteReadPublic,
    PointsReadPublic,
    SignUpFormReadPublic,
)
from app.features.attendance.schemas import (
    GroupReadPublic,
    TrainingReadPublic,
    TrainingTimeReadPublic,
)
from app.features.communication.schemas import RequestReadPublic, ResponseReadPublic
from app.features.guardian.schemas import GuardianReadPublic
from app.features.item.schemas import ItemReadPublic, ItemTypeReadPublic
from app.features.meet.schemas import (
    CategoryReadPublic,
    DisciplineReadPublic,
    DisciplineTypeReadPublic,
    MeetEventReadPublic,
    MeetReadPublic,
)
from app.features.organizator.schemas import HelperReadPublic
from app.features.payment.schemas import PaymentReadPublic
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
    "helper": HelperReadPublic,
    "sign_up_form_group": SignUpFormGroupReadPublic,
    "athlete_registration_meet_event": AthleteRegistrationMeetEventReadPublic,
    "payment": PaymentReadPublic,
    "request": RequestReadPublic,
    "response": ResponseReadPublic,
    "points": PointsReadPublic,
    "file": FileReadPublic,
    "request_file": RequestFileReadPublic,
}
