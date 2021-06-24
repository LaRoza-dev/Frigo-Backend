# %% initialization

print (" type the ingredients that you have available. acceptable choices are : dough , cheese , meat , tomato sauce , pasta , bread. please type the exact same spelling spaces included or result won't be valid. No Capital letters. system can take 3 ingredients ")

recepies = {
	"Pizza" : ['tomato sauce','cheese','dough'],
	"Red pasta":['meat','pasta','tomato sauce'],
	"hamburger":['bread','cheese','meat']
}

for recepie in recepies:
    print(recepies[recepie])





input_list=[]

msg=""
while True:
	msg =input("\nEnter ingredient: ")
	if msg=="done":
		break
	input_list.append(msg)
for recepie in recepies:
	if set(recepies[recepie]).issubset(input_list):
		print(f"\nYou can make {recepie}!")
	elif set(recepies[recepie]).intersection(input_list):
		print(f"\nyou can make {recepie} but need to buy: ")
		print(*[f'{item},' for item in recepies[recepie] if item not in input_list], sep=' ')
