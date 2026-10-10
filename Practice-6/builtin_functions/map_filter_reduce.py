from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Map
squared = list(map(lambda x: x ** 2, numbers))
print(squared)

# Filter
even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)

# Reduce
total = reduce(lambda x, y: x + y, numbers)
print(total)
