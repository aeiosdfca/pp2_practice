#1 basic class definition (like a blueprint)
class Food:
    name = "kimbap"

print(Food.name)


#2 creating objects from a class
class Country:
    name = "South Korea"
    continent = "Asia"

c1 = Country()
c2 = Country()
print(c1.name, "-", c1.continent)
print(c2.name, "-", c2.continent)


#3 class with multiple objects (same class, many instances)
class Song:
    title = "Birds Of A Feather"

s1 = Song()
s2 = Song()
s3 = Song()

print(s1.title)
print(s2.title)
print(s3.title)


#4 empty class using pass (valid but no content)
class Student:
    pass

student1 = Student()
student2 = Student()

print(student1)
print(student2)
