from pydantic_settings import BaseSettings


class AthleteSettings(BaseSettings):
    TRAINER_QUALIFICATION_MAPPING: dict[int, str] = {
        -1: "Neznámá kvalifikace",
        1: "Trenér 1 třídy",
        2: "Trenér 2 třídy",
        3: "Trenér 3 třídy",
        20: "Trenér začtva",
        30: "Trenér přípravek",
    }

    model_config = {"case_sensitive": True}


athlete_settings = AthleteSettings()
