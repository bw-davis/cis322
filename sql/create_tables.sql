-- Created the one table for users, when the scope of the project expands I will adjust accordingly

create table roles (
	role_pk			serial primary key,
	role 			varchar(32)
);

create table users (
    -- decided to have the username be the primary key to cut down on unnecessary fields
    user_pk         varchar(16) primary key,
    -- wanted to allow for a large password if need be to make user feel comfortable
    password        varchar(32),
    role_fk 		integer REFERENCES roles(role_pk) 
);

create table assets (
	asset_pk		serial primary key,
	asset_tag		varchar(16),
	description		text,
	disposed		boolean default FALSE
);

create table facilities (
	facility_pk		serial primary key,
	name			varchar(32),
	code			varchar(6)
);

create table asset_at (
    asset_fk    integer REFERENCES assets(asset_pk) not null,
    facility_fk integer REFERENCES facilities(facility_pk) not null,
    arrive_dt   timestamp,
    depart_dt   timestamp
);