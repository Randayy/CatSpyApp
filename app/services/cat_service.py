from app.db.connect_db import Session
import requests
from app.schemas.schemas import CatCreate, CatSchema
from app.repositories.cat_repository import CatRepository
from fastapi import HTTPException
from app.db.models import Cat
from app.utils.utils import validate_breed


class CatService:
    """
    This class is responsible for handling the business logic of the Cat model.
    """

    def __init__(self, db: Session):
        self.repository = CatRepository(db)

    def get_cat_by_id(self, cat_id: int) -> Cat:
        cat = self.repository.get_cat_by_id(cat_id)
        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")
        return cat

    def create_cat(self, cat: CatCreate) -> Cat:
        breed = cat.breed
        validate_breed(breed)
        return self.repository.create_cat(cat)

    def get_cat_breed_valid(self, breed: str):
        response = requests.get(f"https://api.thecatapi.com/v1/breeds/search?q={breed}")
        return len(response.json()) > 0

    def delete_cat(self, cat_id: int) -> dict:
        cat = self.get_cat_by_id(cat_id)
        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")
        self.repository.delete_cat(cat)
        return {"message": f"Cat with id {cat_id} sdeleted"}

    def get_list_of_cats(self) -> list:
        cats = self.repository.get_list_of_cats()
        return [CatSchema.from_orm(cat) for cat in cats]

    def update_cat_salary(self, cat_id: int, new_salary: int) -> Cat:
        cat = self.repository.get_cat_by_id(cat_id)
        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")
        cat.salary = new_salary
        return self.repository.update_cat(cat)
