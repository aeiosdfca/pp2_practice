#1 the else keyword catches anything which isn't caught by the preceding conditions
a = 333
b = 20
if a > b:
    print("a is greater than b")
else:
    print("a is equal or lesser than b")


#2 this is also an example of how else works
n = 777777772

if n % 2 == 0:
    print("even")
else:
    print("odd")


#3 indetation is important, codes must be indicated by levels of lines 
a = 111
b = 20
if a > b:
print("it's an error") #this will be an error
else:
print("it's an error")


#4 you can have multiple statements inside an if block and all statements must be indented at the same level, also if and else must be in the same level
age = 21
if age >= 18:
    print("you're now a grown person")
    print("you now have a right to vote")
else:
    print("you're underage")
    print("your parents have responsibility for you and your actions")


#5 the else statement acts as a fallback that executes when none of the preceding conditions are true
password = "qwerty123"

if len(password) < 8:
    print("your password {password} is not good enough!")
else:
    print("you have to write your password")