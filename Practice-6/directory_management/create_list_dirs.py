import os

# Create Directory
os.makedirs("myfolder", exist_ok=True)

# Create Nested Directories
os.makedirs("parent/child", exist_ok=True)

# List Files and Directories
print(os.listdir("."))

# Check Directory
print(os.path.isdir("myfolder"))

# Get Current Directory
print(os.getcwd())
