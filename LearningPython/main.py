# Some simple things in python #

# Numbers #
print("integer #1")
print(7+5.3)

print("integer #2")
print(str(7+250) + "200")


# Strings #
print("string #1")
print('She said "Dont do that"')

print("string #2")
print("She said \"Dont do that\"")

print("string #3")
print('She said \"Dont do that\"')

print("string #4")
print('She said \'Dont do that\'')

print("string #5")
print("she", "said", '"Dont', "do", 'that"')

print("string #6")
print("Hello:Amit".split(":"))

print("string #7")
print("This Cost " + str(5+17) + " Dollars")


# Boolean #
print("boolean #1")
print(5 == 5)

print("boolean #2")
print(5 != 5)

print("boolean #3")
print(5 == 4)

print("boolean #4")
print("True" is str(True))

print("boolean #5")
print("True" is True)


# Arrays #
print("arrays #1")
print("I like " + ["Games", "Tenis", "Football"][1])


# Dictionaries #
print("dictionary #1")
print({"name": "Amit", "age": "25", 2: "Football"}["age"])

print("dictionary #2")
print({"name": "Amit", "age": "25", 2: "Football"}[2])


# Variables #
print("variables #1")
a = 2
b = 4
c = 5 == 8
d = "Hello"
e = ["hello", 4, True]
print(str(a), str(b), str(a+b), str(c), str(d), str(e))


# Built In Functions #
print("Built in functions #1")
a = len([1, 3, 5, 10])
print(a)
b = len("MyLenIs8")
print(b)
c = len(["my", "len", "is", 4])
print(c)


# Convert types #
print("Convert types #1")
print(float("5.3"))
print(bool(True))
print(str(5.76))
print(int(75.3))
print(float(True))


# User defined functions #
print("User defined functions #1")


def my_function(name="Unknown", age=18):
    print("My name is", name, "and my age is", age)


my_function()
my_function("Amit")
my_function(age=25)

print("User defined functions #2")


def infinite_hello(*people):
    for person in people:
        print("Hello", person)


infinite_hello("Amit", "Moshe", "Motti")

print("User defined functions #3")


def returning_function(num1, num2):
    return num1+num2


print("The sum is :", returning_function(10,20))


# if-else statements #
print("if-else statements #1")

check = 4

if check == 2:
    print("Check is 2")
elif not check == 4:
    print("Check is not 4")
else:
    print("Check is 4")


# while loops #
print("while loops #1")
a = ["amit", "nick", "avi"]
for people in a:
    print(people)

print("while loops #2")
run = True
current = 1
while run:
    if current == 10:
        run = False
    else:
        print(current)
        current += 1
