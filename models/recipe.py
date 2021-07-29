from typing import Optional, List, Dict

from pydantic import BaseModel, HttpUrl, Field


class RecipeSchema(BaseModel):
    name: str = Field(...)
    stars: int = Field(...)
    skill: str = Field(...)
    serves: str = Field(...)
    prep_time: str = Field(...)
    url: HttpUrl = Field(...)
    ingredients: List[str] = Field(...)
    cook_steps: List[str] = Field(...)
    nutritions: Dict[str, str] = Field(...)
    user_id: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Beetroot tabbouleh",
                "stars": "1",
                "skill": "Easy",
                "serves": "Serves 2",
                "prep_time": "10 mins",
                "url": "https://www.bbcgoodfood.com/recipes/beetroot-tabbouleh",
                "ingredients":[
                    "250g pouch cooked grains",
                    "2 small beetroots, peeled and quartered",
                    "small bunch of mint, leaves picked, plus extra to serve",
                    "small bunch of parsley, roughly chopped, plus extra to serve",
                    "2 tbsp olive oil, plus extra to serve",
                    "1 lemon, zested and juiced",
                    "2 tomatoes, finely chopped",
                    "1 red onion, finely chopped",
                    "1⁄2 cucumber, finely chopped"
                ],
                "cook_steps": [
                    "Put the kettle on to boil. Tip the grains into a fine mesh sieve, pour over a kettleful of boiling water, over the sink, leave to drain, then tip into a large bowl. Put the beetroot, most of the herbs, the olive oil, lemon juice and 5-6 tbsp cold water in a food processor and blitz until smooth. Season lightly, adding a splash more water to loosen if needed. Mix into the bowl of grains and stir until they are well-coated.",
                    "Toss the tomatoes, onion, cucumber and lemon zest into the grain mixture until combined. Season to taste. Divide between two plates, sprinkle with more herbs and drizzle with a little olive oil."
                ],
                "nutritions": {
                    "kcal": "422",
                    "fat": "17g",
                    "saturates": "3g",
                    "carbs": "50g"
                }
            }
        }


class UpdateRecipeModel(BaseModel):
    name: Optional[str]
    stars: Optional[int]
    skill: Optional[str]
    serves: Optional[str]
    prep_time: Optional[str]
    url: Optional[HttpUrl]
    ingredients: Optional[List[str]]
    cook_steps: Optional[List[str]]
    nutritions: Optional[Dict[str,str]]

    class Config:
        schema_extra = {
            "example": {
                "name": "Beetroot tabbouleh",
                "stars": "5",
                "skill": "Hard",
                "serves": "Serves 12",
                "prep_time": "1hr and 10 mins",
                "url": "https://www.bbcgoodfood.com/recipes/beetroot-tabbouleh",
                "ingredients":[
                    "2 Kg pouch cooked grains",
                    "2 big beetroots, peeled and quartered",
                    "big bunch of mint, leaves picked, plus extra to serve",
                    "big bunch of parsley, roughly chopped, plus extra to serve",
                    "5 tbsp olive oil, plus extra to serve",
                    "2 lemon, zested and juiced",
                    "4 tomatoes, chopped",
                    "2 red onion, chopped",
                    "1⁄2 cucumber, chopped"
                ],
                "cook_steps": [
                    "Put the kettle on to boil. Tip the grains into a fine mesh sieve, pour over a kettleful of boiling water, over the sink, leave to drain, then tip into a large bowl. Put the beetroot, most of the herbs, the olive oil, lemon juice and 5-6 tbsp cold water in a food processor and blitz until smooth. Season lightly, adding a splash more water to loosen if needed. Mix into the bowl of grains and stir until they are well-coated.",
                    "Toss the tomatoes, onion, cucumber and lemon zest into the grain mixture until combined. Season to taste. Divide between two plates, sprinkle with more herbs and drizzle with a little olive oil."
                ],
                "nutritions": {
                    "kcal": "800",
                    "fat": "50g",
                    "saturates": "9g",
                    "carbs": "150g"
                },
                
            }
        }


def ResponseModel(data, message,elapsed=None):
    return {
        "data": [data],
        "code": 200,
        "message": message,
        "count":len(data),
        "time":round(elapsed ,2)
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}