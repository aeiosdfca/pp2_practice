# reading files: read(), readline(), readlines()

# opening the file for reading
with open("sample.txt", "r") as f:
    print("=== read() ===")
    content = f.read()
    print(content)

with open("sample.txt", "r") as f:
    print("\n=== readline() ===")
    line = f.readline()
    while line:
        print(line.strip())
        line = f.readline()

with open("sample.txt", "r") as f:
    print("\n=== readlines() ===")
    lines = f.readlines()
    for line in lines:
        print(line.strip())