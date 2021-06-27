# In[]:
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
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
        j=0
        partial_ratio=fuzz.partial_ratio(recepies[recepie],input_list[j].lower())
        j=j+1
        if set(recepies[recepie]).issubset(input_list) and partial_ratio > 80:
            #print(f"\nYou can make {recepie}!")
            result_complete_recepie.append(recepie)
        elif set(recepies[recepie]).intersection(input_list):
            #print(f"\nyou can make {recepie} but need to buy: ")
            items = [item for item in recepies[recepie] if item not in input_list]
            #print(*[f'{item},' for item in recepies[recepie] if item not in input_list], sep=' ')
            result_incomplete_recepie.append( recepie)
            result_items.append(items)
    return result_complete_recepie,result_incomplete_recepie, result_items
      
# In[]:    
x=searchFood(input_list)
definit_result=x[0]
incomplete_results={}


def Convert(x):
    for i in x:
        j=0
        incomplete_results [x[j+1][j]] = x[j+2][j] 
        incomplete_results [x[j+1][j+1]]= x[j+2][j+1]
        j=j+1
    return incomplete_results
         
print(Convert(x))










