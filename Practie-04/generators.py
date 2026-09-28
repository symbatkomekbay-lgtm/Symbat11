def fun(max):
    cnt = 1
    while cnt <= max:
        yield cnt
        cnt += 1

ctr = fun(5)
for n in ctr:
    print(n)

#2
n = int(input())

def generate_squares(n):
    squares = []
    for i in range(n + 1):
        squares.append(i**2)
    return squares

#youtube.com/watch?v=Qfm6nfz1QNQ

print(generate_squares(n))
