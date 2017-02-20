-- Created the one table for users, when the scope of the project expands I will adjust accordingly

create table users (
    -- decided to have the username be the primary key to cut down on unnecessary fields
    user_pk         varchar(16) primary key,
    -- wanted to allow for a large password if need be to make user feel comfortable
    password        varchar(32)
);