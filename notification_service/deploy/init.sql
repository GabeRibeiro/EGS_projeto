create table notification(
    uid text not null,
    id serial,
    msg text not null,
    primary key (uid, id)
);

create table notificationQueue(
    uid text not null,
    id serial,
    pid int default -1,
    msg text not null,
    primary key (uid, id)
);