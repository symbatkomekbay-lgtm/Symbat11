import os
import shutil

# Create Destination Folder
os.makedirs("destination", exist_ok=True)

# Move File
if os.path.exists("demofile.txt"):
    shutil.move("demofile.txt", "destination/demofile.txt")

# Copy File
if os.path.exists("destination/demofile.txt"):
    shutil.copy("destination/demofile.txt", "copy.txt")

# Rename File
if os.path.exists("copy.txt"):
    os.rename("copy.txt", "renamed.txt")
