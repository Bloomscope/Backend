drop database if exists `proto`;

create database if not exists `proto`;

use `proto`;

create table if not exists `users_type` (
	`id` int not null auto_increment,
    `type` varchar(8),
    `access_level` int default 1,
    primary key(`id`)
);

create table if not exists `plans` (
	`id` int not null auto_increment,
    `plan` varchar(15) not null unique,
    `validity` int not null,
    primary key(`id`)
);

create table if not exists `organization` (
	`id` varchar(32) not null,
    `added_on` datetime default current_timestamp,
    `name` varchar(50) not null,
    `org_id` varchar(16) unique not null,
    `address` varchar(50) not null,
    `added_by` varchar(32) not null,
    primary key(`id`)
);

create table if not exists `user` (
	`id` varchar(32) not null,
    `registered_on` datetime default current_timestamp,
    `fname` varchar(20) not null,
    `mname` varchar(20),
    `lname` varchar(20) not null,
    `dob` date not null,
    `email` varchar(32) not null unique,
    `password` varchar(80) not null,
    `phone` varchar(15) not null,
    `last_logged_in` datetime default current_timestamp,
    `organization_id` varchar(32) default null,
    `user_type_id` int not null default 1,
    `is_verified` boolean default 0,
    `has_added_gaurdians` boolean default 0,
    primary key(`id`),
    foreign key(`user_type_id`) references `users_type`(`id`),
    foreign key(`organization_id`) references `organization`(`id`)
);

-- alter table `organization` add foreign key(`added_by`) references `user`(`id`);-- 

create table if not exists `subscription` (
	`id` varchar(32) not null,
    `subscribed_on` datetime not null default current_timestamp,
    `expires_on` datetime not null,
    `plan_id` int not null,
    `user_id` varchar(32) not null,
    primary key(`id`),
    foreign key(`plan_id`) references `plans`(`id`),
    foreign key(`user_id`) references `user`(`id`) on delete cascade
);

create table if not exists `parent` (
	`id` varchar(32) not null,
    `registered_on` datetime default current_timestamp,
    `fname` varchar(20) not null,
    `mname` varchar(20),
    `lname` varchar(20) not null,
    `email` varchar(32) not null unique,
    `password` varchar(80) not null,
    `phone` varchar(15) not null,
	`relation` varchar(20) not null,
    `last_logged_in` datetime default current_timestamp,
    primary key(`id`)
);

create table if not exists `parent_child` (
	`user_id` varchar(32) not null,
    `parent_id` varchar(32) not null,
    primary key(`user_id`, `parent_id`),
    foreign key(`user_id`) references `user`(`id`) on delete cascade on update cascade,
    foreign key(`parent_id`) references `parent`(`id`) on delete cascade on update cascade
);

create table if not exists `parameters` (
	`id` int not null auto_increment,
    `param_name` varchar(32) unique,
    primary key(`id`)
);

create table if not exists `test` (
	`id` varchar(32) not null,
    `name` varchar(32) not null unique,
    `conducted_on` datetime,
    `questions` longblob not null,
    `duration` int not null, 
    `ends_on` datetime,
    primary key(`id`)
);

create table if not exists `questions` (
	`id` varchar(32) not null,
    `question` longtext,
    `options` longblob not null, -- json serialized data--
    `ans` varchar(5) not null,
    `explanation` longtext,
    `param_id` int not null,
    `added_by_id` varchar(32) not null,
    `has_asked` boolean default 0,
    `asked_on` varchar(32) default null,
    primary key (`id`),
    foreign key(`added_by_id`) references `user`(`id`) on delete cascade,
    foreign key(`param_id`) references `parameters`(`id`) on delete cascade,
    foreign key(`asked_on`) references `test`(`id`) on delete cascade
);

create table if not exists `results` (
	`id` varchar(32) not null,
    `completed_on` datetime default current_timestamp,
    `test_id` varchar(32) not null,
    `responses` longblob not null,
    `user_id` varchar(32) not null,
    primary key(`id`),
    foreign key(`test_id`) references `test`(`id`) on delete cascade,
    foreign key(`user_id`) references `user`(`id`) on delete cascade
);

create table if not exists `announcements` (
	`id` varchar(32) not null,
    `announced_on` datetime default current_timestamp,
    `content` longtext not null,
    `announced_by` varchar(32) not null,
    primary key(`id`),
    foreign key(`announced_by`) references `user`(`id`)
);

create table if not exists `suggestions` (
	`id` int auto_increment not null,
    `suggestion_name` varchar(32) not null unique,
    `param_id` int not null,
    `suggestion` longtext,
    primary key(`id`),
    foreign key(`param_id`) references `parameters`(`id`)
);

create table if not exists `complain` (
	`id` varchar(32) not null,
    `raised_on` datetime default current_timestamp,
    `ticket_id` varchar(8) not null unique,
    `status` varchar(32) default 'pending',
    `reason` text not null,
    `raised_by` varchar(32) not null,
    primary key(`id`),
    foreign key(`raised_by`) references `user`(`id`)
);
