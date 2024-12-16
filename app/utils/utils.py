import requests
from fastapi import HTTPException, status


def validate_breed(breed: str):
    url = "https://api.thecatapi.com/v1/breeds"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to fetch breeds from TheCatAPI",
        )

    breeds = response.json()
    breed_names = [b["name"] for b in breeds]

    if breed not in breed_names:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid breed"
        )
    return True
