#1 basic __init__ method with parameters
class Food:
    def __init__(self, name):
        self.name = name

f1 = Food("tteokbokki")
f2 = Food("ramyun")
f3 = Food("kimbap")

print(f1.name)
print(f2.name)
print(f3.name)


#2 __init__ with multiple parameters
class Country:
    def __init__(self, name, continent):
        self.name = name
        self.continent = continent

c1 = Country("South Korea", "Asia")
c2 = Country("Greece", "Europe")
c3 = Country("Ethiopia", "Africa")

print(c1.name, "-", c1.continent)
print(c2.name, "-", c2.continent)
print(c3.name, "-", c3.continent)


#3 __init__ with default values (optional arguments)
class Song:
    def __init__(self, title="Birds Of A Feather", artist="Billie Eilish"):
        self.title = title
        self.artist = artist

s1 = Song()
s2 = Song("We Don't Talk Anymore", "Charlie Puth & Selena Gomez")

print(s1.title, "-", s1.artist)
print(s2.title, "-", s2.artist)


#4 __init__ with many attributes (like a data container)
class Student:
    def __init__(self, name, grade, school):
        self.name = name
        self.grade = grade
        self.school = school

st1 = Student("Igor", 18, "University")
st2 = Student("Katya", 21, "International University")

print(st1.name, st1.grade, st1.school)
print(st2.name, st2.grade, st2.school)



