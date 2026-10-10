# Enumerate
fruits = ["apple", "banana", "cherry"]

for index, fruit in enumerate(fruits):
    print(index, fruit)

# Enumerate with Start
for index, fruit in enumerate(fruits, start=1):
    print(index, fruit)

# Zip
names = ["Ali", "Aruzhan", "Dana"]
ages = [18, 19, 20]

for name, age in zip(names, ages):
    print(name, age)

# Zip to Dictionary
students = dict(zip(names, ages))
print(students)
