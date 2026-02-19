#1 the *args parameter allows a function to accept any number of positional arguments.
def funkciya(*meows):
    print("type:", type(meows))
    print("breed:", meows[0])
    print("second breed:", meows[1])
    print("all breeds:", meows)

funkciya("british shorthair", "sphynx", "siamese")


#2 the **kwargs parameter allows a function to accept any number of keyword arguments, also you can combine **kwargs, *args with regular arguments
def novaya(nickname, **details):
    print("nickname:", nickname)
    print("additional details:")
    for key, value in details.items():
        print(" ", key + ":", value)

novaya("amir133722810", age = 18, city = "Turksibstan", hobby = "cs")


#3 you can use both *args and **kwargs in the same function, but the order must be: arguments -> args -> kwargs
def anime(title, *seasons, **series):
    print("title name:", title)
    print("seasons:", seasons)
    print("series:", series)

anime("Kimetsu no Yaiba", "1", "2", "3", "4", s1_series = 26, s2_series = "18", s3_series = 11, s4_series = 8)


#4 the * and ** operators can also be used when calling functions to unpack (expand) a list or dictionary into separate arguments.
def dogs(breed, name):
    print("Hello", breed, name)

dog = {"breed": "shiba-inu", "name": "Akito"}
dogs(**dog) 