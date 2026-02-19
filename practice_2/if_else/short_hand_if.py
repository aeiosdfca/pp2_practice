#1 if you have only one statement to execute, you can put it on the same line as the if statement
a = 5252
b = 2
if a > b: print("a is greater than b")


#2 if you have one statement for if and one for else, you can put them on the same line using a conditional expression
x = "meow"
y = "woof"
print("dog") if x == y else print("cat")


#3 only the first true condition will be executed, even if the multiple conditions are true 
a = "kimbap"
b = "tteokbokki"
dish = a if a < b else b
print("dish is", dish)


#4 you can chain conditional expressions, but keep it short so it stays readable:
a = 79
b = 86
print("shemyakin") if a < b else print("suyunbai") if a == b else print("papanin")

#5 ternary operators are particularly useful for simple assignments and return statements
name = ""
display_name = name if name else "guest"
print("hi,", display_name)



