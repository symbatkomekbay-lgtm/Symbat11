#1
import math

n = int(input())

print(math.radians(n))

#2
import math

h = int(input("Height: "))
a = int(input("1st base: "))
b = int(input("2nd base: "))

print(((a + b) / 2) * h)

#3
import math

n = int(input("Number of sides: "))
s = float(input("Length of a side: "))

area = (n * s**2) / (4 * math.tan(math.pi / n))

print(round(area, 3))

#4
b = int(input("base: "))
h = int(input("height: "))

print(h * b)
