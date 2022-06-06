CREATE SCHEMA IF NOT EXISTS user;

DROP TABLE IF EXISTS user.users;
DROP TABLE IF EXISTS user.user_adress;
DROP TABLE IF EXISTS user.user_configs;
DROP TABLE IF EXISTS user.user_default_configs;
DROP TABLE IF EXISTS user.user_password_auth;
DROP TABLE IF EXISTS user.user_external_auth;
DROP TABLE IF EXISTS user.user_device;
DROP TABLE IF EXISTS user.login_history;
DROP TABLE IF EXISTS user.user_role;
DROP TABLE IF EXISTS user.role;
DROP TABLE IF EXISTS user.role_permission;
DROP TABLE IF EXISTS user.permission;
DROP TABLE IF EXISTS user.permission_group;
DROP TABLE IF EXISTS user.user_notification_group;
DROP TABLE IF EXISTS user.notification_group;
DROP TABLE IF EXISTS user.notification;
DROP TABLE IF EXISTS user.user_notification_mets;
DROP TABLE IF EXISTS user.mail_template;

CREATE TABLE user.users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR (255) NOT NULL,
    last_name VARCHAR (255) NOT NULL,
    phone_number VARCHAR (15) NOT NULL,
    email VARCHAR (255) NOT NULL,
    is_created  BOOLEAN NOTNULL DEFAULT false,
    is_verified BOOLEAN NOTNULL DEFAULT false,
    profile_image_url VARCHAR  NOT NULL,
    status VARCHAR (50) NOT NULL,

    UNIQUE (email, phone_number)
);

CREATE TABLE user.user_adress (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR (255) NOT NULL,
    name VARCHAR (500) NOT NULL,
    map_name VARCHAR (255) NOT NULL,
    location_lat VARCHAR (255) NOT NULL,
    location_long VARCHAR (255) NOT NULL,
    country VARCHAR (255) NOT NULL,
    city VARCHAR (255) NOT NULL,
    district VARCHAR (255) NOT NULL,
    ward VARCHAR (255) NOT NULL,

    CONSTRAINT fk_user
        FOREIGN KEY(user_id) 
            REFERENCES user.users(id)
);

CREATE TABLE user.user_configs (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR (255) NOT NULL,
    config JSON NOT NULL,

    CONSTRAINT fk_user
        FOREIGN KEY(user_id) 
            REFERENCES user.users(id)
);

CREATE TABLE user.user_default_configs (
    id SERIAL PRIMARY KEY,
    config: JSON NOT NULL
);

CREATE TABLE user.user_password_auth (
    id SERIAL PRIMARY KEY,
    user_id: VARCHAR (255) NOT NULL,
    username VARCHAR (255) NOT NULL,
    email VARCHAR (255) NOT NULL,
    password VARCHAR (255) NOT NULL,
    is_activate BOOLEAN DEFAULT false,
    update_at TIMESTAMP WITH OUT TIME ZONE,
    create_at TIMESTAMP WITH OUT TIME ZONE DEFAULT now(),
    one_time_password BOOLEAN DEFAULT false,

    UNIQUE ( username, email )
    CONSTRAINT fk_user
        FOREIGN KEY(user_id) 
            REFERENCESuser.users(id)

);

CREATE TABLE user.user_external_auth (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR (255) NOT NULL,
    provider VARCHAR (255) NOT NULL,
    auth_key VARCHAR (255) NOT NULL,
    credential VARCHAR (255),
    device_type JSON,
    UNIQUE ( auth_key )
    CONSTRAINT fk_user
        FOREIGN KEY(user_id) 
            REFERENCESuser.users(id)
);

CREATE TABLE user.user_device (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR (255) NOT NULL,
    firebase_token VARCHAR (255) NOT NULL,
    device_id VARCHAR (255) NOT NULL,
    device_type VARCHAR (255),
    is_activate BOOLEAN,
    
    UNIQUE ( device_id )
    CONSTRAINT fk_user
        FOREIGN KEY(user_id) 
            REFERENCESuser.users(id)
);

CREATE TABLE user.login_history(
    id SERIAL PRIMARY KEY,
    user_id VARCHAR (255) NOT NULL,
    timestamp TIMESTAMP WITH OUT TIME ZONE,
    user_device_id VARCHAR (255) NOT NULL,
    location_lat VARCHAR (255) NOT NULL,
    location_long VARCHAR (255) NOT NULL,
    app_version VARCHAR (255) NOT NULL,
    login_type VARCHAR (255) NOT NULL,
    
    CONSTRAINT fk_user
        FOREIGN KEY(user_id) 
            REFERENCES user.users(id)
    CONSTRAINT fk_user_device
        FOREIGN KEY(user_device_id) 
            REFERENCES user.user_device(id)
);

CREATE TABLE user.role (
    id SERIAL PRIMARY KEY,
    name VARCHAR (255) NOT NULL,
    role_code VARCHAR (255) NOT NULL,
    description VARCHAR (255)
);

CREATE TABLE user.permission_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR (255) NOT NULL,
    description VARCHAR (255) NOT NULL,
    target_info JSON,
    target_service VARCHAR (255)
);

CREATE TABLE user.permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR (255) NOT NULL,
    permission_code VARCHAR (255) NOT NULL,
    description VARCHAR (255) NOT NULL,
    group_id VARCHAR (255) NOT NULL,
    default_enabled BOOLEAN DEFAULT false,

    UNIQUE ( permission_code )
    CONSTRAINT fk_permission_group
        FOREIGN KEY (group_id)
            REFERENCES user.permission_group(id)
);


CREATE TABLE user.user_role (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR (255) NOT NULL,
    role_code VARCHAR (255) NOT NULL,
    is_activate BOOLEAN,
    
    CONSTRAINT fk_user
        FOREIGN KEY(user_id) 
            REFERENCES user.users(id)
    CONSTRAINT fk_role
        FOREIGN KEY(role_code) 
            REFERENCES user.role(id)
);

CREATE TABLE user.role_permission (
    id SERIAL PRIMARY KEY,
    role_code VARCHAR (255) NOT NULL,
    permission_code VARCHAR (255) NOT NULL,
    is_enabled BOOLEAN,
    
    CONSTRAINT fk_role
        FOREIGN KEY(role_code) 
            REFERENCES user.role(id)

    CONSTRAINT fk_permission
        FOREIGN KEY (permission_code)
            REFERENCES user.permission(permission_code)
);


CREATE TABLE user.notification_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR (255) NOT NULL,
    description VARCHAR (255) NOT NULL,
    is_push_noti_supported BOOLEAN DEFAULT false,
    is_mail_noti_supproted BOOLEAN DEFAULT false,
    is_app_noti_supported BOOLEAN DEFAULT false,
    sender_mail_address VARCHAR (255) NOT NULL
);

CREATE TABLE user.mail_template (
    id SERIAL PRIMARY KEY,
    name VARCHAR (255) NOT NULL,
    description VARCHAR (255) NOT NULL,
    html_template TEXT NOT NULL
);

CREATE TABLE user.user_notification_group (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR (255) NOT NULL,
    group_id VARCHAR (255) NOT NULL,
    is_push_noti_enabled BOOLEAN DEFAULT false,
    is_mail_enabled BOOLEAN DEFAULT false,
    is_app_noti_enabled BOOLEAN DEFAULT false,
    
    CONSTRAINT fk_user
        FOREIGN KEY(user_id) 
            REFERENCES user.users(id)

    CONSTRAINT fk_notification_group
        FOREIGN KEY (group_id)
            REFERENCES user.notification_group(id)
);

CREATE TABLE user.notification (
    id SERIAL PRIMARY KEY,
    group_id VARCHAR (255) NOT NULL,
    title VARCHAR (255) NOT NULL,
    subject VARCHAR (255),
    noti_target VARCHAR (255),
    description VARCHAR (255),
    mail_templete_id VARCHAR (255) NOT NULL,
    template_variables JSON,
    data_payload JSON,
    is_push_noti BOOLEAN DEFALT false,
    is_mail_noti BOOLEAN DEFALT false,
    is_app_noti BOOLEAN DEFALT false,

    CONSTRAINT fk_notification_group
        FOREIGN KEY (group_id)
            REFERENCES user.notification_group(id)
    
    CONSTRAINT fk_mail_template
        FOREIGN KEY (group_id)
            REFERENCES user.notification_group(id)
);

CREATE TABLE user.user_notification_group (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR (255) NOT NULL,
    noti_id VARCHAR (255) NOT NULL,
    is_push_noti_sent BOOLEAN DEFAULT false,
    is_mail_sent BOOLEAN DEFAULT false,
    is_app_noti_sent BOOLEAN DEFAULT false,
    is_user_deleted BOOLEAN DEFAULT false,
    seen_date_time VARCHAR (255),
    
    CONSTRAINT fk_user
        FOREIGN KEY(user_id) 
            REFERENCES user.users(id)

    CONSTRAINT fk_notification
        FOREIGN KEY (noti_id)
            REFERENCES user.notification(id)
);