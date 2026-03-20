names = ["Chonguk", "Nana", "Gojo Satoru"]
scores = [85, 90, 78]

# enumerate()
print("pronumerovat:")
for index, name in enumerate(names):
    print(index, name)

# zip()
print("\nzip:")
for name, score in zip(names, scores):
    print(name, score)

# type checking and conversion
value = "123"

print("\ntip:", type(value))

num = int(value)
print("convertirovano to int:", num)

flt = float(value)
print("convertirovano to float:", flt)

# combining zip + enumerate
print("\npronumerovano + zip:")
for i, (name, score) in enumerate(zip(names, scores)):
    print(i, name, score)