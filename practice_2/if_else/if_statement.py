#1 an "if statement" is written by using the if keyword.
a = 111
b = 20
if a > b:
    print("b is lesser than a")


#2  if the condition is true, the code block inside the if statement is executed, but if the condition is false, the code block is skipped.
n = 100
if n > 0:
    print("it's positive")


#3 indetation is important, codes must be indicated by levels of lines 
a = 111
b = 20
if a > b:
print("a is greater than b") #this will be an error


#4 you can have multiple statements inside an if block and all statements must be indented at the same level.
age = 21
if age >= 18:
    print("you're now a grown person")
    print("you now have a right to vote")


#5 it also can work with strings and inputs
were_in_SK = True
if were_in_SK:
    print("welcome back to South Korea!")