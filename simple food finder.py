# In[0]:
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
import uuid


recipes = [
        {
        "id":str(uuid.uuid4()),
        "name" : "Pizza",
        "ingredients" : ["tomato sauce","cheese","dough"],
        "recipes" : " tomato sauce - dough - cheese"
        },
        {
        "id":str(uuid.uuid4()),
        "name" : "hamburger",
        "ingredients" : ["bread","cheese","meat"],
        "recipes" : " asdfsdafdfsgsdf"
        },
        {
        "id":str(uuid.uuid4()),
        "name" : "Red pasta",
        "ingredients" : ["meat","pasta","tomato sauce"],
        "recipes" : " fghfdjhgjkjhkghk"
        },        
        ]


# In[1]:
    
# *** Get input from user
    
input_list=[]

msg=""
while True:
	msg =input("\nEnter ingredient: ")
	if msg=="done":
		break
	input_list.append(msg)

# In[2]:

# *** Search with for and append

# def searchFood(input_list):    
#     results={"Complete Foods":[],"Incomplete Foods":[]}
#     j=0
#     for i in recipes:
#         if set(i["ingredients"]).issubset(input_list):
#             results["Complete Foods"].append(dict(i))
#         elif set(i["ingredients"]).intersection(input_list):
#             items = [item for item in dict(i)["ingredients"] if item not in input_list]
#             results["Incomplete Foods"].append(dict(i))
#             results["Incomplete Foods"][j]["ingredients"] = items
#             j+=1
#     return results

# In[3]:

# *** Search with filter and lambda    

def searchFood(input_list):    
    results={"Complete Foods":[],"Incomplete Foods":[]}
    c_food = list(filter(lambda x: set(x["ingredients"]).issubset(input_list), recipes))
    print(c_food)
    results["Complete Foods"]=list(c_food)
    
    i_food = list(filter(lambda x: (set(x["ingredients"]).intersection(input_list) and not set(x["ingredients"]).issubset(input_list)) , recipes))
    for food in range(len(i_food)):
        i_food[food]["ingredients"] = [ingredient for ingredient in i_food[food]["ingredients"] if ingredient not in input_list]
    print(i_food)
    results["Incomplete Foods"]=list(i_food)
    return results


# In[4]:    
    
# *** Example
    
result = searchFood(input_list)

for food in result["Complete Foods"]:
    print(f"You can make {food['name']} !!!!")

for food in result["Incomplete Foods"]:
    print(f"You can make {food['name']} but you need to buy {food['ingredients']}")
