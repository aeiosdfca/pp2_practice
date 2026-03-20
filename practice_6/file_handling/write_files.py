# writing and appending files
# file modes: w, a, x

# creating and writing (w)
with open("sample.txt", "w") as f:
    f.write("Hello\n")
    f.write("This is a sample file\n")
    f.write("Python file handling\n")

# adding (a)
with open("sample.txt", "a") as f:
    f.write("Appended line 1\n")
    f.write("Appended line 2\n")

# creating a new file (x)
try:
    with open("new_file.txt", "x") as f:
        f.write("hi hi hi bye bye bye\n")
except FileExistsError:
    print("File already exists")