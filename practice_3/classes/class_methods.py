#1 basic class method (prints object data)
class Food:
    def __init__(self, name):
        self.name = name

    def show_food(self):
        print(self.name + " 맛있어요")

f1 = Food("kimchi")
f2 = Food("bibimbap")
f3 = Food("chapche")

f1.show_food()
f2.show_food()
f3.show_food()


#2 method accessing object attributes
class Country:
    def __init__(self, name, continent):
        self.name = name
        self.continent = continent

    def info(self):
        return self.name + " is in " + self.continent

c1 = Country("South Korea", "Asia")
c2 = Country("Germany", "Europe")

print(c1.info())
print(c2.info())


#3 method modifying object attributes
class Student:
    def __init__(self, name, points):
        self.name = name
        self.points = points

    def promote(self):
        self.points += 1

s1 = Student("Igor", 100)
print(s1.points)

s1.promote()
print(s1.points)


#4 special method __str__ (controls print output)
class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

    def __str__(self):
        return self.title + " - " + self.artist

song1 = Song("Radio", "Rammstein")
song2 = Song("Change", "Deftones")

print(song1)
print(song2)
