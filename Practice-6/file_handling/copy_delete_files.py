import os

# Delete File
os.remove("demofile.txt")

# Check if File Exists Before Deleting
if os.path.exists("demofile.txt"):
    os.remove("demofile.txt")
else:
    print("The file does not exist")

# Delete Folder
os.rmdir("myfolder")
