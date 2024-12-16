from sqlalchemy.orm import Session
from app.db.models import Cat


class CatRepository:
    """
    This class is responsible for handling all the database operations related to the Cat model.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_cat_by_id(self, cat_id: int) -> Cat:
        return self.db.query(Cat).filter(Cat.id == cat_id).first()

    def create_cat(self, cat) -> Cat:
        db_cat = Cat(**cat.dict())
        self.db.add(db_cat)
        self.db.commit()
        self.db.refresh(db_cat)
        return db_cat

    def delete_cat(self, cat) -> None:
        self.db.delete(cat)
        self.db.commit()

    def get_list_of_cats(self) -> list:
        return self.db.query(Cat).all()

    def update_cat(self, cat) -> Cat:
        self.db.commit()
        self.db.refresh(cat)
        return cat
