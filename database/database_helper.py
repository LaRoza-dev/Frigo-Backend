# helpers


def recipe_helper(recipe) -> dict:
    return {
        "id": str(recipe["_id"]),
        "name": recipe["name"],
        "stars": recipe["stars"],
        "skill": recipe["skill"],
        "serves": recipe["serves"],
        "prep_time": recipe["prep_time"],
        "url": recipe["url"],
        "ingredients": recipe["ingredients"],
        "cook_steps": recipe["cook_steps"],
        "nutritions": recipe["nutritions"]
    }


def user_helper(user) -> dict:
    return {
        "id": str(user['_id']),
        "fullname": user['fullname'],
        "email": user['email']
    }

def admin_helper(admin) -> dict:
    return {
        "id": str(admin['_id']),
        "fullname": admin['fullname'],
        "email": admin['email']
    }