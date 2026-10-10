# Open a File
f = open("demofile.txt")
print(f.read())

# Open a File from Another Location
f = open("D:\\myfiles\\welcome.txt")
print(f.read())

# Using with Statement
with open("demofile.txt") as f:
    print(f.read())

# Close a File
f = open("demofile.txt")
print(f.readline())
f.close()

# Read First 5 Characters
with open("demofile.txt") as f:
    print(f.read(5))

# Read One Line
with open("demofile.txt") as f:
    print(f.readline())

# Read Two Lines
with open("demofile.txt") as f:
    print(f.readline())
    print(f.readline())

# Read File Line by Line
with open("demofile.txt") as f:
    for x in f:
        print(x)
