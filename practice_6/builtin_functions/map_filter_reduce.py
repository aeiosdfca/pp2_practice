from functools import reduce

numbers = [3, 5, 4, 1, 2, 6, 7]

# map()
squared = list(map(lambda x: x**2, numbers))
print("v kvadrate:", squared)

# filter()
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("chetnie:", evens)

# reduce()
sum_all = reduce(lambda x, y: x + y, numbers)
print("summa:", sum_all)

# built-in functions
print("dlina:", len(numbers))
print("min:", min(numbers))
print("maks:", max(numbers))
print("otsortirovano v obratnom:", sorted(numbers, reverse=True))