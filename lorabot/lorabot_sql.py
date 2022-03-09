sql_queries = {
    "user_check": '''SELECT 1 FROM lorabot.users WHERE user_id = %(user_id)s and bot_id = %(bot_id)s''',
    "user_insert": '''INSERT INTO lorabot.users (user_id, bot_id, language_code) VALUES (%(user_id)s, %(bot_id)s, 
                      %(language_code)s)''',
    "message": '''INSERT INTO lorabot.messages (message, user_id, message_type, bot_id) 
                  VALUES (%(message)s,%(user_id)s, %(message_type)s, %(bot_id)s)''',
    "event": '''INSERT INTO lorabot.events (event, user_id, event_type, bot_id) 
                VALUES (%(event)s, %(user_id)s, %(event_type)s, %(bot_id)s)''',
    "assessment": '''INSERT INTO lorabot.bot_rating (assessment, user_id, bot_id)
                     VALUES (%(assessment)s,%(user_id)s, %(bot_id)s)''',
    "review": '''INSERT INTO lorabot.bot_rating (review, user_id, bot_id) VALUES(%(review)s,%(user_id)s, %(bot_id)s)''',
    "analyze_total": '''            SELECT 'Total users' as info, COUNT(*) 
                                    FROM lorabot.users  WHERE bot_id = %(bot_id)s
                                    UNION ALL
                                    SELECT 'Total messages' as info, COUNT(*) 
                                    FROM lorabot.messages  WHERE bot_id = %(bot_id)s
                                    UNION ALL
                                    SELECT 'Total events' as info, COUNT(*) 
                                    FROM lorabot.events  WHERE bot_id = %(bot_id)s
                                    UNION ALL
                                    SELECT 'AVG number of messages per users all time' as info, ROUND(COALESCE(AVG(amount),0) ,2)
                                    FROM(
                                    SELECT user_id, COUNT(*) as amount 
                                    FROM lorabot.messages WHERE bot_id = %(bot_id)s
                                    GROUP BY user_id) as tab
                                    UNION ALL
                                    SELECT 'AVG number of messages per users in day' as info, ROUND(COALESCE(AVG(amount), 0) ,2)
                                    FROM(
                                    SELECT user_id, message_time::date, COUNT(*) as amount 
                                    FROM lorabot.messages WHERE bot_id = %(bot_id)s
                                    GROUP BY 1,2) as tab
                                    UNION ALL
                                    SELECT 'AVG number of event per users all time' as info, ROUND(COALESCE(AVG(amount), 0), 2)
                                    FROM(
                                    SELECT user_id, COUNT(*) as amount 
                                    FROM lorabot.events WHERE bot_id = %(bot_id)s
                                    GROUP BY user_id) as tab
                                    UNION ALL
                                    SELECT 'AVG number of event per users in day' as info, ROUND(COALESCE(AVG(amount), 0), 2)
                                    FROM(
                                    SELECT user_id, event_time::date, COUNT(*) as amount 
                                    FROM lorabot.events WHERE bot_id = %(bot_id)s
                                    GROUP BY 1,2) as tab ''',
    "analyze_user_number_accumulation": '''    SELECT user_time as date,
                                               coalesce(sum(sub_amount) over (order by user_time rows between 
                                               unbounded preceding and current row),0) as amount
                                               FROM (
                                               SELECT user_time::date, COUNT(*) as sub_amount
                                               FROM lorabot.users WHERE bot_id = %(bot_id)s
                                               GROUP BY 1
                                               ) as tab;''',
    "analyze_new_user": '''SELECT user_time::date AS date , count(user_id) AS amount 
                           FROM lorabot.users WHERE bot_id = %(bot_id)s
                           GROUP BY 1 ORDER BY 1''',
    "analyze_hour_activity": '''SELECT CAST(date_part('hour', message_time) AS INTEGER) as "hour",
                                count(*) FILTER (WHERE EXTRACT(dow FROM message_time) = 0) AS sun,
                                count(*) FILTER (WHERE EXTRACT(dow FROM message_time) = 1) AS mon,
                                count(*) FILTER (WHERE EXTRACT(dow FROM message_time) = 2) AS tue,
                                count(*) FILTER (WHERE EXTRACT(dow FROM message_time) = 3) AS wed,
                                count(*) FILTER (WHERE EXTRACT(dow FROM message_time) = 4) AS thu,
                                count(*) FILTER (WHERE EXTRACT(dow FROM message_time) = 5) AS fri,
                                count(*) FILTER (WHERE EXTRACT(dow FROM message_time) = 6) AS sat
                                FROM lorabot.messages WHERE bot_id = %(bot_id)s
                                GROUP BY 1
                                ORDER BY 1;''',
    "analyze_dau": ''' SELECT message_time::date AS date, count(distinct user_id) AS amount 
                       FROM lorabot.messages WHERE bot_id = %(bot_id)s 
                       GROUP BY 1 ORDER BY 1 ''',
    "analyze_wau": ''' SELECT CAST(EXTRACT(WEEK FROM message_time) AS VARCHAR)as date,count(distinct user_id) AS amount 
                       FROM lorabot.messages WHERE bot_id = %(bot_id)s
                       GROUP BY EXTRACT(YEAR FROM message_time), EXTRACT(MONTH FROM message_time), 
                       EXTRACT(WEEK FROM message_time) 
                       ORDER BY EXTRACT(YEAR FROM message_time), EXTRACT(MONTH FROM message_time), 
                       EXTRACT(WEEK FROM message_time)''',
    "analyze_mau": '''SELECT CAST(EXTRACT(MONTH FROM message_time) AS VARCHAR) AS date, 
                      count(distinct user_id) AS amount 
                      FROM lorabot.messages WHERE bot_id = %(bot_id)s
                      GROUP BY EXTRACT(YEAR FROM message_time), EXTRACT(MONTH FROM message_time) 
                      ORDER BY EXTRACT(YEAR FROM message_time), EXTRACT(MONTH FROM message_time)''',
    "analyze_yau": '''SELECT CAST(EXTRACT(YEAR FROM message_time) AS VARCHAR)as date, count(distinct user_id) AS amount
                      FROM lorabot.messages WHERE bot_id = %(bot_id)s
                      GROUP BY EXTRACT(YEAR FROM message_time)
                      ORDER BY EXTRACT(YEAR FROM message_time)''',
    "analyze_messages_number": '''SELECT message_time::date AS date, count(*) AS amount 
                                  FROM lorabot.messages WHERE bot_id = %(bot_id)s
                                  GROUP BY 1
                                  ORDER BY 1''',
    "analyze_messages": '''SELECT message, count(*) AS volume FROM lorabot.messages WHERE bot_id = %(bot_id)s
                           GROUP BY 1
                           ORDER BY 2 desc''',
    "analyze_messages_type": '''SELECT message_type AS type, count(*) AS amount 
                                FROM lorabot.messages WHERE bot_id = %(bot_id)s
                                GROUP BY 1
                                ORDER BY 1''',
    "analyze_events_number": '''SELECT event_time::date AS date, count(*) AS amount 
                                FROM lorabot.events WHERE bot_id = %(bot_id)s
                                GROUP BY 1
                                ORDER BY 1''',
    "analyze_events": '''SELECT event, count(*) AS volume FROM lorabot.events WHERE bot_id = %(bot_id)s
                         GROUP BY 1
                         ORDER BY 2 desc''',
    "analyze_events_type": '''SELECT event_type AS type, count(*) AS amount 
                              FROM lorabot.events WHERE bot_id = %(bot_id)s
                              GROUP BY 1
                              ORDER BY 1''',
    "analyze_events_funnel": '''SELECT event, COUNT(*) as amount
                                FROM lorabot.events WHERE bot_id = %(bot_id)s 
                                GROUP BY 1
                                ORDER BY 1''',
    "analyze_messages_funnel": '''SELECT message, COUNT(*) as amount
                                  FROM lorabot.messages WHERE bot_id = %(bot_id)s 
                                  GROUP BY 1
                                  ORDER BY 1''',
    "analyze_assessment": '''SELECT assessment , count(*) AS amount 
                             FROM lorabot.bot_rating WHERE bot_id = %(bot_id)s and assessment is not null
                             GROUP BY 1
                             ORDER BY 2 desc ''',
    "analyze_review": '''SELECT review FROM lorabot.bot_rating WHERE bot_id = %(bot_id)s and review is not null
                         ORDER BY rate_time desc''',
    "analyze_language": '''SELECT language_code AS type, count(*) AS amount 
                           FROM lorabot.users WHERE bot_id = %(bot_id)s
                           GROUP BY 1
                           ORDER BY 2 desc''',
    "analyze_bots_users": '''SELECT bot_id, count(*) from lorabot.users 
                             group by bot_id order by 2 desc''',
    "check_schema_and_tables": '''SELECT count(*) AS amount FROM information_schema.tables
                                  WHERE  table_schema = 'lorabot' '''
}
sql_ddl = {
    "create": '''create schema lorabot;

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
'''}