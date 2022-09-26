
import traceback
from loguru import logger
from typing import Tuple, AnyStr
from core.types.failure import Failure
from core.utils.hash import hash_password
from core.modules.sql_module import create_database_tables
from ...domain.repository import UserRepository
from ..dao import UserDAO
from ...domain.entities import User

class UserRepositoryImpl(UserRepository):
    def __init__(self) -> None:
        super().__init__()

        self.user_dao = UserDAO()

    async def init(self):
        await create_database_tables()


    def _delete_additional_keys(self, entity: dict, secondary_field: str = None, fk: bool = True):
        if '_sa_instance_state' in entity:
            del entity['_sa_instance_state']
        entity['id'] = str(entity.get('id'))
        if secondary_field:
            entity[secondary_field] = str(entity.get(secondary_field))

    def _handle_object(self, instance: dict, secondary_field: str = None):
        self._delete_additional_keys(entity=instance, secondary_field=secondary_field,fk=False)
        return instance

    async def create_user(self, data: dict, *args, **kwargs) -> Tuple[User, Failure]:
        try:
            data.update({"password":hash_password(data["password"].decode("utf8"))})
            user_orm = self.user_dao.create(**data)
            user = await self.user_dao.save(user_orm)
            return user, None
        except Exception as exc:
            logger.error(f"ERROR: {traceback.format_exc()}")
            return None, Failure(400, str(exc.__cause__))

    