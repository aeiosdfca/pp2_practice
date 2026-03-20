import shutil
import os

# copying the file
shutil.copy("sample.txt", "sample_copy.txt")

# creating a backup
shutil.copy("sample.txt", "backup_sample.txt")

print("file skopirovan uspeshno")

# safe deleting
file_to_delete = "backup_sample.txt"

if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"{file_to_delete} deleted")
else:
    print("file ne nayden")