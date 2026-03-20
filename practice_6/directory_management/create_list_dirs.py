import os

# current directory
print("tekushaya directoriya:", os.getcwd())

# creating a folder
os.mkdir("test_dir")

# craeting nested folder
os.makedirs("test_dir/nested_dir/sub_dir")

# list of folders and files
print("\nsoderzhanie directorii:")
print(os.listdir())

# go to the directory
os.chdir("test_dir")
print("\nizmenennaya directoriya:", os.getcwd())

# empty folders deleting
os.chdir("..")
os.rmdir("test_dir/nested_dir/sub_dir")
os.rmdir("test_dir/nested_dir")