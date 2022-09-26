
from datetime import datetime
from typing import Dict
"""
Just control the dependencies of Entities here
"""
class BaseEntity(object):

    def to_json(self, keys=None) -> Dict:
        return {k: v for k, v in self.__dict__.items() if not '__' in k and (keys is None or k in keys)}
    
        # super().__init__()

"""
Common Entitity with common fields
"""
# @dataclass(init=False, kw_only=True)
class CommonEntity(BaseEntity):
    id: str
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    is_deleted: bool
    deleted_at: datetime
    deleted_by: str

    # def __init__(self, **kwargs):
    #     names = set([f.name for f in dataclasses.fields(self)])
    #     for k, v in kwargs.items():
    #         if k in names and isinstance(v, UUID):
    #             setattr(self, k, str(v))
    #         elif k in names:
    #             setattr(self, k, v)


# @dataclass
class StringDetailEntity(BaseEntity):
    language: str
    name: str
    description: str