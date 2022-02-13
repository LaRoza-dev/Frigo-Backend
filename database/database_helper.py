# helpers


def recipe_helper(recipe) -> dict:
    return {
        "id": str(recipe["_id"]),
        "name": recipe["name"],
        "introduction": recipe["introduction"],
        "stars": recipe["stars"],
        "skill": recipe["skill"],
        "serves": recipe["serves"],
        "prep_time": recipe["prep_time"],
        "cook_time": recipe["cook_time"],
        "url": recipe["url"],
        "ingredients": recipe["ingredients"],
        "cook_steps": recipe["cook_steps"],
        "nutritions": recipe["nutritions"],
        "user_id":recipe["user_id"],
    }


def user_helper(user) -> dict:
    return {
        "id": str(user['_id']),
        "fullname": user.get('fullname'),
        "email": user.get('email'),
        "is_admin":user.get('is_admin'),
        "fridge":user.get('fridge') or [],
        "wishlist":user.get('wishlist') or [],
        "birthdate":user.get('birthdate') or None,
        "gender":user.get('gender') or None
        
    }

