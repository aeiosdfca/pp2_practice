#1 with the while loop code can be executed as a set of statements as long as a condition is true
count = 1
while count < 25:
    print(count)
    count += 1


#2 with the break statement we can stop the loop even if the while condition is true
age = 1
while age < 25:
    print(age)
    if age == 18:
        break
    age += 1


#3 with the continue statement we can stop the current iteration, and continue with the next
room = 101
while room < 777:
    room += 11
    if room == 666:
        continue
    print(room)

#with the else statement we can run a block of code once when the condition no longer is true
id = 1000000
while id < 2000000:
    print(id)
    id += 100000
else:
    print("id is no longer less than 200000")

