# In[]:
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
    
# In[]:

    

def searchFood(input_list):
    result_complete_recepie = []
    result_incomplete_recepie = []
    result_items = []
    
    for recepie in recepies:
        if set(recepies[recepie]).issubset(input_list):
            print(f"\nYou can make {recepie}!")
            result_complete_recepie.append(recepie)
        elif set(recepies[recepie]).intersection(input_list):
            print(f"\nyou can make {recepie} but need to buy: ")
            items = [item for item in recepies[recepie] if item not in input_list]
            print(*[f'{item},' for item in recepies[recepie] if item not in input_list], sep=' ')
            result_incomplete_recepie.append( recepie)
            result_items.append(items)
    return result_complete_recepie,result_incomplete_recepie, result_items
      
# In[]:      
x=searchFood(input_list)
















