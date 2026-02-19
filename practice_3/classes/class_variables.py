#1 Basic class variable (shared by all objects)
class Food:
    category = "Korean food"   

    def __init__(self, name):
        self.name = name       

f1 = Food("tteokbokki")
f2 = Food("ramyun")

print(f1.name, "-", f1.category)
print(f2.name, "-", f2.category)


# #2 Changing class variable (affects all objects)
class Country:
    planet = "Earth"

    def __init__(self, name):
        self.name = name

c1 = Country("South Korea")
c2 = Country("Japan")

Country.planet = "Mars"   

print(c1.name, "-", c1.planet)
print(c2.name, "-", c2.planet)


#3 Instance variable overrides class variable
class Song:
    genre = "Rock"   

    def __init__(self, title):
        self.title = title

s1 = Song("Smells Like Teen Spirit")
s2 = Song("PA PA YA")

s2.genre = "Metal"   

print(s1.title, "-", s1.genre)
print(s2.title, "-", s2.genre)


#4 Class variable as a counter (common OOP example)
class Student:
    total_students = 0   

    def __init__(self, name):
        self.name = name
        Student.total_students += 1

st1 = Student("Igor")
st2 = Student("Venera")
st3 = Student("Katya")

print("Total students:", Student.total_students)
