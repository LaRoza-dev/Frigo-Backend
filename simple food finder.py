# In[]:
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
import uuid


recepies = {
	"Pizza" : ['tomato sauce','cheese','dough'],
	"Red pasta":['meat','pasta','tomato sauce'],
	"hamburger":['bread','cheese','meat']
}

# In[]:
input_list=[]

msg=""
while True:
	msg =input("\nEnter ingredient: ")
	if msg=="done":
		break
	input_list.append(msg)

# In[]
def searchFood(input_list):
    results={'Complete Foods':{},'Incomplete Foods':{}}

    for recepie in recepies:
        # partial_ratio=fuzz.partial_ratio(recepies[recepie],input_list[j].lower())
        if set(recepies[recepie]).issubset(input_list): #and partial_ratio > 80:
            results['Complete Foods'].update({recepie :{ 'id': uuid.uuid4()}})
        elif set(recepies[recepie]).intersection(input_list):
            items = [item for item in recepies[recepie] if item not in input_list]
            results['Incomplete Foods'].update({recepie:{'Items':items, 'id': uuid.uuid4()}})
    return results
      
# In[]:    
results =searchFood(input_list)

for food in results['Complete Foods'].keys():
    print(f'You can make {food} !!!!')

for food in results['Incomplete Foods'].keys():
    print(f'You can make {food} but you need to buy {results["Incomplete Foods"][food]["Items"]}')


