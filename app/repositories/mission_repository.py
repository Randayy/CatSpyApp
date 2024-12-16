from sqlalchemy.orm import Session
from app.db.models import Mission


class MissionRepository:
    """
    This class is responsible for handling all the database operations related to the Mission model.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_mission(self, mission: Mission) -> Mission:
        self.db.add(mission)
        self.db.commit()
        self.db.refresh(mission)
        return mission

    def get_mission_by_id(self, mission_id: int) -> Mission:
        return self.db.query(Mission).filter(Mission.id == mission_id).first()

    def delete_mission(self, mission: Mission) -> None:
        self.db.delete(mission)
        self.db.commit()

    def update_mission(self, mission: Mission) -> Mission:
        self.db.commit()
        self.db.refresh(mission)
        return mission

    def get_list_of_missions(self) -> list:
        return self.db.query(Mission).all()
