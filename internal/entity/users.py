
from sqlalchemy import UniqueConstraint, ForeignKey, func, Column, String, TEXT, BOOLEAN, JSON, TIMESTAMP
from sqlalchemy.orm import relationship
from internal.entity.base import BaseEntity
from internal.entity.mixin import TimestampMixin


class Users(BaseEntity, TimestampMixin):

    __table_args__ = (
        UniqueConstraint('phone_number'),
        UniqueConstraint('email'),
    )

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    phone_number = Column(String(255), index=True, nullable=False)
    email = Column(String(255), index=True, nullable=False)
    is_created = Column(BOOLEAN, default=False)
    is_verified = Column(BOOLEAN, default=False)
    profile_image_url = Column(TEXT, nullable=False)
    status = Column(String(50), nullable=False)


class User_adress(BaseEntity, TimestampMixin):
    user_id = Column(String(255), ForeignKey(Users.id))
    name = Column(String(255), nullable=False)
    map_name = Column(String(255), nullable=False)
    location_lat = Column(String(255), nullable=False)
    location_long = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    district = Column(String(255), nullable=False)
    ward = Column(String(255), nullable=False)

class User_configs(BaseEntity, TimestampMixin):
    user_id = Column(String(255), ForeignKey(Users.id))
    config = Column(JSON, nullable=False)

class User_default_configs(BaseEntity, TimestampMixin):
    config = Column(JSON, nullable=False)

class user_password_auth(BaseEntity, TimestampMixin):
    __table_args__ = (
        UniqueConstraint('username'),
        UniqueConstraint('email'),
    )

    user_id = Column(String(255), ForeignKey(Users.id))
    username = Column(String(255), nullable=False)
    email = Column(String(255), index=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_activate = Column(BOOLEAN, default=False)
    update_at = Column(TIMESTAMP(timezone=False), nullable=True)
    create_at = Column(TIMESTAMP(timezone=False), default=func.now())
    one_time_password = Column(BOOLEAN, default=False)

class User_external_auth(BaseEntity, TimestampMixin):
    __table_args__=(
        UniqueConstraint('auth_key'),
    )

    user_id = Column(String(255), ForeignKey(Users.id))
    provider = Column(String(255), nullable=False)
    auth_key = Column(String(255), nullable=False)
    credential = Column(String(255), nullable=True)
    device_type = Column(JSON)

class User_device(BaseEntity, TimestampMixin):
    __table_args__=(
        UniqueConstraint('device_id'),
    )

    user_id = Column(String(255), ForeignKey(Users.id))
    firebase_token = Column(String(255), nullable=False)
    device_id = Column(String(255), nullable=False)
    device_type = Column(String(255), nullable=True)
    is_activate  = Column(BOOLEAN)

class Login_history(BaseEntity, TimestampMixin):
    user_id = Column(String(255), ForeignKey(Users.id))
    user_device_id = Column(String(255), ForeignKey(User_device.id))
    timestamp = Column(TIMESTAMP(timezone=False))
    location_lat = Column(String(255), nullable=False)
    location_long = Column(String(255), nullable=False)
    app_version = Column(String(255), nullable=True)
    login_type = Column(String(255), nullable=True)


class Role(BaseEntity, TimestampMixin):
    name = Column(String(255), nullable=False)
    role_code = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

class Permission_group(BaseEntity, TimestampMixin):
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    target_info = Column(JSON, nullable=False)
    target_sercive = Column(String(255), nullable=False)

class Permission(BaseEntity, TimestampMixin):
    __table_args__=(
        UniqueConstraint('permission_code'),
    )
    name = Column(String(255), nullable=False)
    permission_code = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    group_id = Column(String(255), ForeignKey(Permission_group.id))
    default_enable = Column(BOOLEAN, default=False)

class User_role(BaseEntity, TimestampMixin):
    user_id = Column(String(255), ForeignKey(Users.id))
    group_id = Column(String(255), ForeignKey(Permission_group.id))
    is_activate  = Column(BOOLEAN)

class Role_permission(BaseEntity):
    role_code = Column(String(255), ForeignKey(Role.id))
    permission_code = Column(String(255), ForeignKey(Permission.permission_code))
    is_enabled = Column(BOOLEAN)
    

class Notification_group(BaseEntity, TimestampMixin):
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    is_push_noti_supported = Column(BOOLEAN, default=False)
    is_mail_noti_supproted = Column(BOOLEAN, default=False)
    is_app_noti_supported = Column(BOOLEAN, default=False)
    sender_mail_address = Column(String(255), nullable=False)

class Mail_template(BaseEntity, TimestampMixin):
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    html_template = Column(TEXT, nullable=False)

class User_notification_group(BaseEntity, TimestampMixin):
    user_id = Column(String(255), ForeignKey(Users.id))
    group_id = Column(String(255), ForeignKey(Notification_group.id))
    is_push_noti_enabled = Column(BOOLEAN, default=False)
    is_mail_enabled = Column(BOOLEAN, default=False)
    is_app_noti_enabled = Column(BOOLEAN, default=False)

class Notification(BaseEntity, TimestampMixin):
    group_id = Column(String(255), ForeignKey(Notification_group.id))
    title = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=True)
    noti_taget = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    mail_template_id = Column(String(255), ForeignKey(Mail_template.id))
    template_variables = Column(JSON)
    data_payload = Column(JSON)
    is_push_noti = Column(BOOLEAN, default=False)
    is_mail_noti = Column(BOOLEAN, default=False)
    is_app_noti = Column(BOOLEAN, default=False)

class User_notification_mets(BaseEntity, TimestampMixin):
    user_id = Column(String(255), ForeignKey(Users.id))
    noti_id = Column(String(255), ForeignKey(Notification.id))
    is_push_noti_sent = Column(BOOLEAN, default=False)
    is_mail_sent = Column(BOOLEAN, default=False)
    is_app_noti_sent = Column(BOOLEAN, default=False)
    is_user_deleted = Column(BOOLEAN, default=False)
    seen_date_time = Column(String(255))
