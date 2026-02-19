#1 the elif keyword allows you to check multiple expressions for True and execute a block of code as soon as one of the conditions evaluates to True
a = 3333
b = 3333
if a > b:
    print("a is greater than b")
elif a == b:
    print("a and b are equal")


#2 you can use multiple "elif"s if you need
points = 100

if points >= 90:
    print("grade A")
elif points >= 80:
    print("grade B")
elif points >= 70:
    print("grade C")
elif points >= 60:
    print("grade D")
else:
    print("grade F")


#3 only the first true condition will be executed, even if the multiple conditions are true 
age = 18

if age < 13:
    print("child")
elif age < 20:
    print("teenager")
elif age < 65:
    print("adult")
elif age < 100:
    print("senior")
else:
    print("probably dead")


#4 use elif when you have multiple mutually exclusive conditions to check 
day = 24
day %= 7

if day == 1:
  print("Monday")
elif day == 2:
  print("Tuesday")
elif day == 3:
  print("Wednesday")
elif day == 4:
  print("Thursday")
elif day == 5:
  print("Friday")
elif day == 6:
  print("Saturday")
elif day == 7:
  print("Sunday")

