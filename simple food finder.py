


print (" type the ingredients that you have available. acceptable choices are : dough , cheese , meat , tomato sauce , pasta , bread. please type the exact same spelling spaces included or result won't be valid. No Capital letters. system can take 3 ingredients ")



first_ingredient = input("\nFirst ingredient: ")
second_ingredient = input("\nSecond ingredient: ")
third_ingredient = input("\nThird ingredient: ")



Pizza = ['cheese','dough','tomato sauce']
Red_pasta = ['meat','pasta','tomato sauce']
Hamburgur = ['bread','cheese','meat']
input_list=['a','b','c']
input_list[0] = first_ingredient
input_list[1] = second_ingredient
input_list[2] = third_ingredient
input_list.sort()

if Pizza == input_list:
	print("\nYou can make pizza!")
if Red_pasta == input_list:
	print("\nYou can make red pasta!")
if Hamburgur == input_list:
	print("\nYou can make hamburgur!")

input()
	
