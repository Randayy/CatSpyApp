from fastapi import FastAPI, Depends, HTTPException
from app.db.connect_db import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List
from app.db.connect_db import get_db
from app.services.mission_service import MissionService
from app.schemas.schemas import MissionSchema, MissionCreate, MissionBase
from fastapi import APIRouter

mission_router = APIRouter()

@mission_router.post("/create", response_model=MissionBase)
def create_mission(mission: MissionCreate, db: Session = Depends(get_db)) -> MissionBase:
    service = MissionService(db)
    return service.create_mission(mission)

@mission_router.get("/list")
def get_list_of_missions(db: Session = Depends(get_db)):
    service = MissionService(db)
    return service.get_list_of_missions()

@mission_router.delete("/delete_all")
def delete_all_missions(db: Session = Depends(get_db)) -> dict:
    service = MissionService(db)
    return service.delete_all_missions()

@mission_router.get("/{mission_id}", response_model=MissionSchema)
def get_mission_by_id(mission_id: int, db: Session = Depends(get_db)) -> MissionSchema:
    service = MissionService(db)
    return service.get_mission_by_id(mission_id)

@mission_router.delete("/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)) -> dict:
    service = MissionService(db)
    return service.delete_mission(mission_id)


@mission_router.put("/{mission_id}/asign_cat/{cat_id}")
def asign_cat_to_mission(mission_id: int, cat_id: int, db: Session = Depends(get_db)) -> dict:
    service = MissionService(db)
    return service.asign_cat_to_mission(mission_id, cat_id)

@mission_router.put("/{mission_id}/complete_target/{target_id}")
def update_status_of_target_to_completed(mission_id: int, target_id: int, db: Session = Depends(get_db)) -> dict:
    service = MissionService(db)
    return service.update_status_of_target_to_completed(mission_id, target_id)

@mission_router.put("/{mission_id}/change_notes/{target_id}")
def change_notes_of_target(new_notes: str,mission_id: int, target_id: int, db: Session = Depends(get_db)) -> dict:
    service = MissionService(db)
    return service.update_notes_of_target(mission_id, target_id, new_notes)

@mission_router.put("/{mission_id}/complete_mission")
def complete_mission(mission_id: int, db: Session = Depends(get_db)) -> dict:
    service = MissionService(db)
    return service.complete_mission(mission_id)
