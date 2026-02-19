#1 boolean can take values True and False only
print(77 > 1)
print(77 == 1)
print(77 < 1)


#2 comparison of two variables
a = 333
b = 24

if b < a:
  print("b is lesser than a")
else:
  print("b is not lesser than a")


#3 evaluating values and variables
print(bool("hi"))
print(bool(18))


#4 evaluating other variables
x = "hi"
y = 18

print(bool(x))
print(bool(y))


#5 evaluating types of variables
z = "bye"
w = 1111

print(type(bool(z)))
print(type(bool(w)))