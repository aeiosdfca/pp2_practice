#1 parent class, inheritance basics
class Food:
    def __init__(self, name):
        self.name = name

    def show_food(self):
        print(self.name, "감사합니다")


# Child class inherits from Food
class KoreanFood(Food):
    pass

f1 = KoreanFood("kimchi_chigae")
f2 = KoreanFood("dakgalbi")

f1.show_food()
f2.show_food()


#2 parent class, super function
class Person:
    def __init__(self, name, country):
        self.name = name
        self.country = country

    def info(self):
        print(self.name, "from", self.country)


# child class
class Student(Person):
    def __init__(self, name, country, course):
        super().__init__(name, country)  
        self.course = course

    def student_info(self):
        print(self.name, "is in course", self.course)


s1 = Student("Igor", "Kazakhstan", "PP2")
s1.info()
s1.student_info()


#3 parent class, overriding
class Animal:
    def speak(self):
        print("The animal makes a sound")


# child overrides parent method
class Cat(Animal):
    def speak(self):
        print("Meow")


class Dog(Animal):
    def speak(self):
        print("Woof")


a = Animal()
c = Cat()
d = Dog()

a.speak()
c.speak()
d.speak()


#4 overriding with extra behavior using super()
class Song:
    def play(self):
        print("Playing a song")


class KpopSong(Song):
    def play(self):
        super().play()
        print("K-pop version is playing")


song1 = KpopSong()
song1.play()


#5 two parent classes, multiple inheritance
class Country:
    def show_country(self):
        print("Country: South Korea")


class Music:
    def show_music(self):
        print("Music genre: K-pop")


# child inherits from TWO classes
class Idol(Country, Music):
    def name(self):
        print("Idol: Daehen")


idol1 = Idol()
idol1.show_country()
idol1.show_music()
idol1.name()


