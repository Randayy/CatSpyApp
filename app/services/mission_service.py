from app.db.models import Mission, Target
from app.schemas.schemas import MissionCreate, MissionSchema
from app.repositories.mission_repository import MissionRepository
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.cat_service import CatService
from fastapi import status


class MissionService:
    """
    This class is responsible for handling the business logic of the Mission model.
    """

    def __init__(self, db: Session):
        self.mission_repository = MissionRepository(db)
        self.cat_service = CatService(db)

    def create_mission(self, mission: MissionCreate) -> Mission:
        if not (1 <= len(mission.targets) <= 3):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The number of targets must be between 1 and 3",
            )

        targets = [Target(**target.dict()) for target in mission.targets]
        mission_data = Mission(**mission.dict(exclude={"targets"}), targets=targets)
        return self.mission_repository.create_mission(mission_data)

    def get_mission_by_id(self, mission_id: int) -> Mission:
        mission = self.mission_repository.get_mission_by_id(mission_id)
        if not mission:
            raise HTTPException(status_code=404, detail="Mission not found")
        return mission
    
    def get_list_of_missions(self) -> list:
        missions = self.mission_repository.get_list_of_missions()
        return [MissionSchema.from_orm(mission) for mission in missions]

    def delete_mission(self, mission_id: int) -> dict:
        mission = self.get_mission_by_id(mission_id)
        self.mission_repository.delete_mission(mission)
        return {"message": f"Mission with id {mission_id} deleted"}

    def check_if_cat_have_mission(self, cat_id: int) -> bool:
        missions = self.mission_repository.get_list_of_missions()
        for mission in missions:
            if mission.cat_id == cat_id:
                return True
        return False

    def asign_cat_to_mission(self, mission_id: int, cat_id: int) -> dict:
        if self.check_if_cat_have_mission(cat_id):
            raise HTTPException(status_code=400, detail="Cat already has a mission")
        mission = self.get_mission_by_id(mission_id)
        self.cat_service.get_cat_by_id(cat_id)
        mission.cat_id = cat_id
        self.mission_repository.update_mission(mission)
        return {
            "message": f"Cat with id {cat_id} assigned to mission with id {mission_id}"
        }

    def update_status_of_target_to_completed(
        self, mission_id: int, target_id: int
    ) -> dict:
        mission = self.get_mission_by_id(mission_id)
        target = next(
            (target for target in mission.targets if target.id == target_id), None
        )
        if not target:
            raise HTTPException(status_code=404, detail="Target not found")
        if self.check_if_all_mission_targets_completed(mission_id):
            self.complete_mission(mission_id)
        target.complete = True
        self.mission_repository.update_mission(mission)
        return {
            "message": f"Target with id {target_id} in mission with id {mission_id} completed"
        }

    def complete_mission(self, mission_id: int) -> dict:
        mission = self.get_mission_by_id(mission_id)
        if self.check_if_mission_completed(mission_id):
            raise HTTPException(status_code=400, detail="Mission is already completed")
        if not self.check_if_all_mission_targets_completed(mission_id):
            raise HTTPException(
                status_code=400, detail="All targets in the mission must be completed"
            )
        mission.complete = True
        self.mission_repository.update_mission(mission)
        return {"message": f"Mission with id {mission_id} completed"}

    def check_if_mission_completed(self, mission_id: int) -> bool:
        mission = self.get_mission_by_id(mission_id)
        if mission.complete == True:
            return True
        return False

    def check_if_target_completed(self, mission_id: int, target_id: int) -> bool:
        mission = self.get_mission_by_id(mission_id)
        target = next(
            (target for target in mission.targets if target.id == target_id), None
        )
        if target.complete == True:
            return True
        return False

    def check_if_all_mission_targets_completed(self, mission_id: int) -> bool:
        mission = self.get_mission_by_id(mission_id)
        for target in mission.targets:
            if target.complete == False:
                return False
        return True

    def update_notes_of_target(
        self, mission_id: int, target_id: int, new_notes: str
    ) -> dict:
        mission = self.get_mission_by_id(mission_id)
        if self.check_if_mission_completed(mission_id):
            raise HTTPException(status_code=400, detail="Mission is already completed")
        target = next(
            (target for target in mission.targets if target.id == target_id), None
        )
        if not target:
            raise HTTPException(status_code=404, detail="Target not found")
        if self.check_if_target_completed(mission_id, target_id):
            raise HTTPException(status_code=400, detail="Target is already completed")
        target.notes = new_notes
        self.mission_repository.update_mission(mission)
        return {
            "message": f"Notes updated for target with id {target_id} in mission with id {mission_id}"
        }
        
        
    def delete_all_missions(self) -> dict:
        missions = self.mission_repository.get_list_of_missions()
        for mission in missions:
            self.mission_repository.delete_mission(mission)
        return {"message": "All missions deleted"}
