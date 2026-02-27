# example with built-in math functions (min, max, abs, round, pow)

cifri = [10, -3, 7, 2]
print(min(cifri), max(cifri))  
print(abs(-7.25), pow(2, 3), round(3.14159, 2))  


# math module functions (sqrt, ceil, floor, sin, cos, pi, e)

import math
print(math.sqrt(64), math.ceil(1.4), math.floor(1.4))  
print(math.sin(math.pi/2), math.pi, math.e)        


# math with random module (random, randint, choice, shuffle)

import random
print(random.random(), random.randint(1,100)) 
items = ['a', 'b', 'c', 'd']
print(random.choice(items))  
random.shuffle(items)
print(items)  



