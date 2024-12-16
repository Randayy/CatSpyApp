# app/schemas.py

from pydantic import BaseModel
from typing import List, Optional


class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = None
    complete: bool = False


class TargetCreate(TargetBase):
    pass


class Target(TargetBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class CatBase(BaseModel):
    name: str
    breed: str
    years_of_experience: int
    salary: int


class CatCreate(CatBase):
    pass


class CatSchema(CatBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class CatUpdateSalary(BaseModel):
    salary: int


class MissionBase(BaseModel):
    cat_id: int
    complete: bool = False
    targets: List[TargetBase]


class MissionCreate(MissionBase):
    targets: List[TargetCreate]


class MissionSchema(MissionBase):
    id: int
    targets: List[Target]

    class Config:
        orm_mode = True
        from_attributes = True
