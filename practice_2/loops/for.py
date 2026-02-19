#1 a for loop is used for iterating over a sequence and even strings are iterable objects, they contain a sequence of characters
k_dishes = ["kimchi", "tteokbokki", "sundae"]
for i in k_dishes:
    print(i)

for i in "blablablablewblewblewblueblueblue":
    print(i)


#2 with the break statement we can stop the loop before it has looped through all the items:
j_dishes = ["sushi", "ramen", "yakisoba", "lagman"]
for i in j_dishes:
    print(i)
    if i == "lagman":
        break

j_dishes = ["sushi", "ramen", "yakisoba", "lagman"]
for i in j_dishes:
    if i == "lagman":
        break
    print(i)


#3 with the continue statement we can stop the current iteration of the loop, and continue with the next
k_dishes = ["kimchi", "tteokbokki", "plov", "sundae"]
for i in k_dishes:
    if i == "plov":
        continue
    print(i)


#4 range function sets the range of for loop work, also can be added the start/end points and the step
for i in range(5):
    print(i)

for i in range(2, 10):
    print(i)

for i in range(2, 20, 4):
    print(i)

#5 else also can be used, nested loops are possible, and can be skipped if error is expected
for i in range(5):
  print(i)
else:
  print("next is five")


taste = ["salty", "spicy", "umami"]
k_dishes = ["kimchi", "tteokbokki", "sundae"]

for i in taste:
    for j in k_dishes:
        print(i, j)


for i in [0, 10, 30]:
    pass