-- Created the one table for users, when the scope of the project expands I will adjust accordingly

create table roles (
	role_pk			serial primary key,
	role 			varchar(32)
);
insert into roles (role) values ('Logistics Officer');
insert into roles (role) values('Facilities Officer');
create table users (
    -- decided to have the username be the primary key to cut down on unnecessary fields
    user_pk         varchar(16) primary key,
    -- wanted to allow for a large password if need be to make user feel comfortable
    password        varchar(32),
    role_fk 		integer REFERENCES roles(role_pk) 
);
-- create table to store asset data
create table assets (
	asset_pk		serial primary key,
	asset_tag		varchar(16),
	description		text,
	disposed		boolean default FALSE	-- when an asset is disposed of this is set to true
);
-- create table to store facility data
create table facilities (
	facility_pk		serial primary key,
	name			varchar(32),
	code			varchar(6)
);
-- this table will tell us which facilities assets are at, when they arrived and when they depart
create table asset_at (
    asset_fk    integer REFERENCES assets(asset_pk) not null,
    facility_fk integer REFERENCES facilities(facility_pk) not null,
    arrive_dt   timestamp default now(),
    depart_dt   timestamp. -- when an asset is disposed of this get's filled in
);
