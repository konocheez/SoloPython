

name = input("What's your name? ")
#takes user input value and stores it in name
#input function takes string to prompt user

print("Hello " + name + "!")

age = input("How old are you? ")

year = input("What year is it? ")

birthyear = int(year) - int(age)

bday = input("Has your birthday passed? y/n ")

if bday == 'y':
    print("So you were born in the year " + str(birthyear) + "?")
else:
    print("So you were born in the year " + str(birthyear-1) + "?")
