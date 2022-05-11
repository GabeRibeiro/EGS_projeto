create table notification(
    uid int not null,
    id serial,
    msg text not null,
    primary key (uid, id)
);

create table notificationQueue(
    uid int not null,
    id serial,
    pid int default -1,
    msg text not null,
    primary key (uid, id)
);