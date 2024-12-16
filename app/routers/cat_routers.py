from fastapi import FastAPI, Depends, HTTPException
from app.db.connect_db import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List
from app.db.connect_db import get_db
from app.services.cat_service import CatService
from app.schemas.schemas import CatCreate, CatSchema, CatUpdateSalary, CatBase
from fastapi import APIRouter

cat_router = APIRouter()


@cat_router.post("/create", response_model=CatBase)
def create_cat(cat: CatCreate, db: Session = Depends(get_db)) -> CatBase:
    service = CatService(db)
    return service.create_cat(cat)


@cat_router.get("/list")
def get_list_of_cats(db: Session = Depends(get_db)) -> list:
    service = CatService(db)
    cats = service.get_list_of_cats()
    return cats


@cat_router.get("/{cat_id}", response_model=CatSchema)
def get_cat_by_id(cat_id: int, db: Session = Depends(get_db)) -> CatSchema:
    service = CatService(db)
    return service.get_cat_by_id(cat_id)


@cat_router.delete("/{cat_id}")
def delete_cat(cat_id: int, db: Session = Depends(get_db)) -> dict:
    service = CatService(db)
    return service.delete_cat(cat_id)


@cat_router.put("/{cat_id}/update_salary", response_model=CatSchema)
def update_cat_salary(
    cat_id: int, cat_update: CatUpdateSalary, db: Session = Depends(get_db)
) -> CatSchema:
    service = CatService(db)
    return service.update_cat_salary(cat_id, cat_update.salary)
