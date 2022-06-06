DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS user_address;
DROP TABLE IF EXISTS user_defalt_configs;
DROP TABLE IF EXISTS user_configs;
DROP TABLE IF EXISTS user_password_auths;
DROP TABLE IF EXISTS user_external_auths;
DROP TABLE IF EXISTS uses_devices;
DROP TABLE IF EXISTS login_histories;
DROP TABLE IF EXISTS user_roles;
DROP TABLE IF EXISTS role_permission;
DROP TABLE IF EXISTS permission_groups;
DROP TABLE IF EXISTS user_notification_groups;
DROP TABLE IF EXISTS notification_groups;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS user_notification_metas;
DROP TABLE IF EXISTS mail_templates;

CREATE TABLE users (
	id serial PRIMARY KEY,
	first_name VARCHAR NOT NULL (255),
	last_name VARCHAR NOT NULL (255),
    email VARCHAR NOT NULL (500),
    phone_number VARCHAR NOT NULL (15),
    is_created BOOLEAN NOT NULL DEFAULT false,
	is_verified BOOLEAN NOT NULL DEFAULT false,
    status VARCHAR,
    create_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    UNIQUE(email, phone_number)
);

CREATE TABLE user_address (
	id serial PRIMARY KEY,
    user_id VARCHAR NOT NULL ,
	first_name VARCHAR NOT NULL (255),
	last_name VARCHAR NOT NULL (255),
    email VARCHAR NOT NULL (500),
    phone_number VARCHAR NOT NULL (15),
    is_created BOOLEAN NOT NULL DEFAULT false,
	is_verified BOOLEAN NOT NULL DEFAULT false,
    status VARCHAR,
    create_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    UNIQUE(email, phone_number)
);




CREATE TABLE user_password_auths (
	id serial PRIMARY KEY,
    user_id VARCHAR NOT NULL,
	username VARCHAR NOT NULL (255),
    email VARCHAR NOT NULL (500),
    password VARCHAR NOT NULL (15),
    is_active BOOLEAN NOT NULL DEFAULT false,
    create_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    create_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    UNIQUE(email, username)
);

INSERT INTO public.users
(first_name, last_name, birth_date, gender, email, phone_number, address, is_admin, create_at)
VALUES('Minh Ngoc', 'Hoang', '1996-11-24', 'male', 'ngochm@ohio-digital.com', '0988389396', 'Duong Dinh Nghe, Yen Hoa, Cau Giay, Ha Noi', true, now());
