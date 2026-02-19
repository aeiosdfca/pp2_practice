#1 AND operator returns True if both statements are true
x = 4
print(x < 5 and x < 25)


#2 OR operator returns True if one of the statements is true
w = 27
print(w < 5 or w > 25)


#3 NOT operator reverses the result, returns False if the result is true
z = 11
print(not(z < 5 and z < 25))


#4 can be combined in the more complex one
p = 11
print(not(p < 16 and p < 26)or(p < 22 and p < 23 or not(p < 14)))


#5 it also can work with strings and inputs
username = input("enter your name: ")
display_name = username or "guest" 
print("hello, " + display_name)