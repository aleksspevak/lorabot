create schema lorabot;

create table if not exists lorabot.users
(
    use_key       bigserial
        constraint pk_users
            primary key,
    user_id       bigint                                         not null,
    bot_id        varchar                                        not null,
    user_time     timestamp default CURRENT_TIMESTAMP(0)         not null,
    language_code varchar   default 'not set'::character varying not null
);

create table if not exists lorabot.messages
(
    mes_key      bigserial
        constraint pk_messages
            primary key,
    user_id      bigint                                 not null,
    bot_id       varchar                                not null,
    message_time timestamp default CURRENT_TIMESTAMP(0) not null,
    message      varchar                                not null,
    message_type varchar                                not null
);

create table if not exists lorabot.events
(
    eve_key    bigserial
        constraint pk_events
            primary key,
    user_id    bigint                                 not null,
    bot_id     varchar                                not null,
    event_time timestamp default CURRENT_TIMESTAMP(0) not null,
    event      varchar                                not null,
    event_type varchar                                not null
);


create table if not exists lorabot.bot_rating
(
    rat_key    bigserial
        constraint pk_bot_rating
            primary key,
    user_id    bigint  not null,
    bot_id     varchar not null,
    rate_time  timestamp default CURRENT_TIMESTAMP(0),
    review     varchar,
    assessment integer
);
