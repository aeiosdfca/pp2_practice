import shutil
import os

# creating the folder for moving
os.makedirs("destination", exist_ok=True)

# moving the file
if os.path.exists("sample.txt"):
    shutil.move("sample.txt", "destination/sample.txt")
    print("fayl peremeshen")

# copying back
shutil.copy("destination/sample.txt", "sample_copy_again.txt")
print("fayl skopirovan obratno")

# searching for files
print("\nishem for txt files")
for file in os.listdir("destination"):
    if file.endswith(".txt"):
        print(file)