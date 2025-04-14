

BEGIN;

CREATE TABLE IF NOT EXISTS public.club (
        id text NOT NULL,
        name text NOT NULL,
        description text NOT NULL,
        created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS public.remote_config
(
    id int NOT NULL,
    urgent_message text,
    minimum_app_version text NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE Schema IF NOT EXISTS tenant_id;

CREATE TABLE IF NOT EXISTS tenant_id.school_year
(
    id uuid NOT NULL,
    name text NOT NULL,
    PRIMARY KEY (id),

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.athlete_status
(
    id uuid NOT NULL,
    name text NOT NULL,
    description text,
    PRIMARY KEY (id),

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.guardian
(
    id uuid NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    email text NOT NULL,
    phone text NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (email),
    UNIQUE (phone),
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.item_type
(
    id uuid NOT NULL,
    name text NOT NULL,
    PRIMARY KEY (id),

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.item
(
    id uuid NOT NULL,
    name text NOT NULL,
    description text,
    image text,
    count smallint NOT NULL,
    item_type_id uuid NOT NULL,
    athlete_id uuid,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.athlete
(
    id uuid NOT NULL,
    birth_number text NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    street text NOT NULL,
    city text NOT NULL,
    zip text NOT NULL,
    email text,
    phone text,
    ean text,
    note text,
    club_id text,
    profile_picture text,
    athlete_status_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (email),
    UNIQUE (phone),
    UNIQUE (ean),
    UNIQUE (birth_number),
    UNIQUE (profile_picture),
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);


CREATE TABLE IF NOT EXISTS tenant_id.athlete_guardian
(
    athlete_id uuid NOT NULL,
    guardian_id uuid NOT NULL,

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.trainer_status
(
    id uuid NOT NULL,
    name text NOT NULL,
    description text,
    PRIMARY KEY (id),

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.trainer
(
    id uuid NOT NULL,
    athlete_id uuid NOT NULL,
    trainer_status_id uuid NOT NULL,
    qualification text NOT NULL,
    salary_per_hour smallint NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (athlete_id),
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

/* CREATE TABLE IF NOT EXISTS tenant_id.athlete_item
(
    athlete_id uuid NOT NULL,
    item_id uuid NOT NULL,

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL); */



CREATE TABLE IF NOT EXISTS tenant_id.web_post
(
    id uuid NOT NULL,
    title text NOT NULL,
    content text NOT NULL,
    trainer_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id."group"
(
    id uuid NOT NULL,
    name text NOT NULL,
    description text,
    training_time_id uuid NOT NULL,
    school_year_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.group_athlete
(
    group_id uuid NOT NULL,
    athlete_id uuid NOT NULL,

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.group_trainer
(
    group_id uuid NOT NULL,
    trainer_id uuid NOT NULL,

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.training
(
    id uuid NOT NULL,
    datetime_ timestamp with time zone NOT NULL,
    group_id uuid NOT NULL,
    description text,
    duration_minutes smallint NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.training_time
(
    id uuid NOT NULL,
    day text NOT NULL,
    summer_time time with time zone NOT NULL,
    winter_time time with time zone NOT NULL,
    PRIMARY KEY (id),

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.training_athlete
(
    training_id uuid NOT NULL,
    athlete_id uuid NOT NULL,
    presence text NOT NULL,

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.training_trainer
(
    training_id uuid NOT NULL,
    trainer_id uuid NOT NULL,
    presence text,

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.sign_up_form
(
    id uuid NOT NULL,
    birth_number text NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    street text NOT NULL,
    city text NOT NULL,
    zip text NOT NULL,
    email text,
    phone text,
    guardian_first_name1 text NOT NULL,
    guardian_last_name1 text NOT NULL,
    guardian_first_name2 text,
    guardian_last_name2 text,
    guardian_phone1 text NOT NULL,
    guardian_email1 text NOT NULL,
    guardian_phone2 text,
    guardian_email2 text,
    note text,
    sign_up_form_status_id uuid NOT NULL,
    school_year_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.sign_up_form_status
(
    id uuid NOT NULL,
    name text NOT NULL,
    description text,
    PRIMARY KEY (id),

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.discipline
(
    id smallint NOT NULL,
    discipline_type_id smallint NOT NULL,
    description text NOT NULL,
    short_description text NOT NULL,
    description_en text NOT NULL,
    short_description_en text NOT NULL,
    PRIMARY KEY (id),

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.discipline_type
(
    id smallint NOT NULL,
    name text NOT NULL,
    description text,
    name_en text,
    description_en text,
    PRIMARY KEY (id),

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.meet
(
    id text NOT NULL,
    name text NOT NULL,
    start_at timestamp with time zone NOT NULL,
    end_at timestamp with time zone NOT NULL,
    location text,
    organizer text,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.meet_event
(
    id uuid NOT NULL,
    meet_id text NOT NULL,
    meet_type text NOT NULL,
    discipline_id smallint NOT NULL,
    category_id smallint NOT NULL,
    start_at timestamp with time zone NOT NULL,
    phase text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    PRIMARY KEY (id),
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.category
(
    id smallint NOT NULL,
    sex smallint NOT NULL,
    description text NOT NULL,
    short_description text NOT NULL,
    description_en text NOT NULL,
    short_description_en text NOT NULL,
    PRIMARY KEY (id),

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.athlete_meet_event
(
    athlete_id uuid NOT NULL,
    meet_event_id uuid NOT NULL,
    result text,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

CREATE TABLE IF NOT EXISTS tenant_id.athlete_sign_up_form
(
    athlete_id uuid NOT NULL,
    sign_up_form_id uuid NOT NULL,

    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL);

/* Foreign keys */

ALTER TABLE IF EXISTS tenant_id.item
    ADD FOREIGN KEY (item_type_id)
    REFERENCES tenant_id.item_type (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.athlete
    ADD FOREIGN KEY (athlete_status_id)
    REFERENCES tenant_id.athlete_status (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.athlete_guardian
    ADD FOREIGN KEY (athlete_id)
    REFERENCES tenant_id.athlete (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.athlete_guardian
    ADD FOREIGN KEY (guardian_id)
    REFERENCES tenant_id.guardian (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.trainer
    ADD FOREIGN KEY (athlete_id)
    REFERENCES tenant_id.athlete (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.trainer
    ADD FOREIGN KEY (trainer_status_id)
    REFERENCES tenant_id.trainer_status (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.athlete_item
    ADD FOREIGN KEY (athlete_id)
    REFERENCES tenant_id.athlete (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.athlete_item
    ADD FOREIGN KEY (item_id)
    REFERENCES tenant_id.item (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.web_post
    ADD FOREIGN KEY (trainer_id)
    REFERENCES tenant_id.trainer (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id."group"
    ADD FOREIGN KEY (school_year_id)
    REFERENCES tenant_id.school_year (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id."group"
    ADD FOREIGN KEY (training_time_id)
    REFERENCES tenant_id.training_time (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.group_athlete
    ADD FOREIGN KEY (group_id)
    REFERENCES tenant_id."group" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.group_athlete
    ADD FOREIGN KEY (athlete_id)
    REFERENCES tenant_id.athlete (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.group_trainer
    ADD FOREIGN KEY (group_id)
    REFERENCES tenant_id."group" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.group_trainer
    ADD FOREIGN KEY (trainer_id)
    REFERENCES tenant_id.trainer (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.training
    ADD FOREIGN KEY (group_id)
    REFERENCES tenant_id."group" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.training_athlete
    ADD FOREIGN KEY (training_id)
    REFERENCES tenant_id.training (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.training_athlete
    ADD FOREIGN KEY (athlete_id)
    REFERENCES tenant_id.athlete (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.training_trainer
    ADD FOREIGN KEY (training_id)
    REFERENCES tenant_id.training (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.training_trainer
    ADD FOREIGN KEY (trainer_id)
    REFERENCES tenant_id.trainer (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.sign_up_form
    ADD FOREIGN KEY (sign_up_form_status_id)
    REFERENCES tenant_id.sign_up_form_status (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.sign_up_form
    ADD FOREIGN KEY (school_year_id)
    REFERENCES tenant_id.school_year (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.discipline
    ADD FOREIGN KEY (discipline_type_id)
    REFERENCES tenant_id.discipline_type (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.meet_event
    ADD FOREIGN KEY (category_id)
    REFERENCES tenant_id.category (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.meet_event
    ADD FOREIGN KEY (discipline_id)
    REFERENCES tenant_id.discipline (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.meet_event
    ADD FOREIGN KEY (meet_id)
    REFERENCES tenant_id.meet (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.meet_event
    ADD FOREIGN KEY (meet_type)
    REFERENCES tenant_id.meet (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.athlete_meet_event
    ADD FOREIGN KEY (athlete_id)
    REFERENCES tenant_id.athlete (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.athlete_meet_event
    ADD FOREIGN KEY (meet_event_id)
    REFERENCES tenant_id.meet_event (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.athlete_sign_up_form
    ADD FOREIGN KEY (athlete_id)
    REFERENCES tenant_id.athlete (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS tenant_id.athlete_sign_up_form
    ADD FOREIGN KEY (sign_up_form_id)
    REFERENCES tenant_id.sign_up_form (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

alter table if exists tenant_id.group_trainer add primary key (group_id, trainer_id);
alter table if exists tenant_id.group_athlete add primary key (group_id, athlete_id);
alter table if exists tenant_id.training_athlete add primary key (training_id, athlete_id);
alter table if exists tenant_id.training_trainer add primary key (training_id, trainer_id);
alter table if exists tenant_id.athlete_guardian add primary key (athlete_id, guardian_id);
/*alter table if exists tenant_id.athlete_item add primary key (athlete_id, item_id);*/
alter table if exists tenant_id.athlete_meet_event add primary key (athlete_id, meet_event_id);
alter table if exists tenant_id.athlete_sign_up_form add primary key (athlete_id, sign_up_form_id);


END;