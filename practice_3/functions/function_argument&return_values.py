#1 information can be passed into functions as arguments, where "name" is a parameter, and "kimbap" is argument
def FoodNames(name):
    print(name + " 맛있어요")

FoodNames("tteokbokki")
FoodNames("ramyun")
FoodNames("kimbap")


#2 you can add as much parameters as you want and also set the default value for them
def country(name = "South Korea", side = "Asia"):
    print("I'm from", name, "it's in", side)

country("Japan", "Asia")
country("Iceland", "Europe")
country("New Zealand", "Oceania")
country()


#3 functions can return any data type, including lists, tuples, dictionaries, and more
def k_dishes():
    return ["jeyuk_bokkeum", "dak_galbi", "kimchi_jjigae"]

dishes = k_dishes()
print("first one is: ", dishes[0])
print("second one is: ", dishes[1])
print("third one is: ", dishes[2])


#4 arguments before / are positional-only, and arguments after * are keyword-only
def numbers(x, y, /, *, w, z):
  return (x + y) * (w + z)

result = numbers(67, 69, w = 7, z = 18)
print(result)