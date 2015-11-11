-- constraints.sql
alter table legal_entities add primary key (lei);
alter table legal_entities add unique (legal_name);
alter table legal_entities alter column legal_name set not null;
alter table legal_entities alter column legal_address_line1 set not null;
alter table legal_entities alter column legal_address_city set not null;
alter table legal_entities alter column legal_address_country set not null;
alter table legal_entities alter column hq_address_line1 set not null;
alter table legal_entities alter column hq_address_city set not null;
alter table legal_entities alter column hq_address_country set not null;
alter table legal_entities alter column entity_status set not null;
alter table legal_entities alter column initial_registration_date set not null;
alter table legal_entities alter column last_update_date set not null;
alter table legal_entities alter column registration_status set not null;
alter table legal_entities alter column next_renewal_date set not null;
alter table legal_entities alter column managing_lou set not null;
