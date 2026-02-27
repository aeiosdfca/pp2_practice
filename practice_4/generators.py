# example of using iter() and next()

eats = ["oats", "wheat", "rice"]
it = iter(eats)               
print(next(it))                  
print(next(it))                  
print(next(it))        


# looping through an iterator

for grain in eats:
    print(grain)


# creating an iterator

class chetnieNumbers:
    def __iter__(self):
        self.n = 2
        return self
    def __next__(self):
        x = self.n
        self.n += 2
        return x

even_iter = iter(chetnieNumbers())
print(next(even_iter))  
print(next(even_iter))  
print(next(even_iter))  


# generators with yield keyword and creating generator functions

def prosto_gen():
    yield "아"
    yield "우"
    yield "에"

k = prosto_gen()
print(next(k))  
print(next(k))  
print(next(k))  


# generator expressions

fourth_dimension = (x*x*x*x for x in range(7))
print(list(fourth_dimension))