create table products (
    product_pk  serial primary key,
    vendor      text,
    description text,
    alt_description text,
    product_name    varchar(128),
    product_model   varchar(128),
    price           numeric
);
create table assets (
    asset_pk    serial primary key,
    product_fk  integer REFERENCES products(product_pk) not null,
    asset_tag   varchar(32),
    description text,
    alt_description text
);
create table vehicles (
    vehicle_pk  serial primary key,
    asset_fk    integer REFERENCES assets(asset_pk) not null
);
create table facilities (
    facility_pk serial primary key,
    fcode   varchar(16),
    common_name varchar(128),
    location    varchar(128)
);
create table asset_at (
    asset_fk    integer REFERENCES assets(asset_pk) not null,
    facility_fk integer REFERENCES facilities(facility_pk) not null,
    arrive_dt   timestamp,
    depart_dt   timestamp
);
create table convoys (
    convoy_pk   serial primary key,
    request varchar(16),
    source_fk   integer REFERENCES facilities(facility_pk) not null,
    dest_fk integer REFERENCES facilities(facility_pk) not null,
    depart_dt   timestamp,
    arrive_dt   timestamp
);
create table used_by (
    vehicle_fk  integer REFERENCES vehicles(vehicle_pk) not null,
    convoy_fk   integer REFERENCES convoys(convoy_pk) not null
);
create table asset_on (
    asset_fk    integer REFERENCES assets(asset_pk) not null,
    convoy_fk   integer REFERENCES convoys(convoy_pk) not null,
    load_dt timestamp,
    unload_dt   timestamp
);
create table users (
    user_pk         serial primary key,
    username        varchar(64),
    active          boolean default FALSE 
);
create table roles (
    role_pk         serial primary key,
    title           varchar(32)
);
create table user_is (
    user_fk         integer REFERENCES users(user_pk) not null,
    role_fk         integer REFERENCES roles(role_pk) not null
);
create table user_supports (
    user_fk         integer REFERENCES users(user_pk) not null,
    facility_fk     integer REFERENCES facilities(facility_pk) not null
);
create table levels (
    level_pk        serial primary key,
    abbrv           varchar(3),
    comment         varchar(128)
);
create table compartments (
    compartment_pk  serial primary key,
    abbrv           varchar(8),
    comment         varchar(128)
);
create table security_tags (
    tag_pk          serial primary key,
    level_fk        integer REFERENCES levels(level_pk) not null,
    compartment_fk  integer REFERENCES compartments(compartment_pk) not null,
    user_fk         integer REFERENCES users(user_pk) not null,
    asset_fk        integer REFERENCES assets(asset_pk),
    product_fk      integer REFERENCES products(product_pk) not null
);