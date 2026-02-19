#1 lambda is a small anonymous function
plus = lambda x, y: x + y
print(plus(6, 7))

square = lambda w: w * w
print(square(11))


#2 map() applies a function to every item in an iterable
ciferki = [9, 18, 27, 36, 45]

ciferki_v_kube = list(map(lambda x: x ** 3, ciferki))
print(ciferki_v_kube) 

foods = ["tteokbokki", "ramyun", "kimbap"]
upper_foods = list(map(lambda x: x.upper(), foods))
print(upper_foods)


#3 filter() selects elements that satisfy a condition
numbers = [11, 121, 12, 144, 13, 169]

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)   

long_foods = list(filter(lambda x: len(x) > 6, foods))
print(long_foods)     


#4 sorted() can use lambda as a custom key
countries = [("South Korea", 51), ("Japan", 125), ("Iceland", 0.3), ("New Zealand", 5)]

sorted_countries = sorted(countries, key=lambda x: x[1])
print(sorted_countries)

sorted_foods = sorted(foods, key=lambda x: len(x))
print(sorted_foods)
