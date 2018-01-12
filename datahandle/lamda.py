
# lamdba has no return statement, the last expression takes over

def f(x): 
    return x **2

print(f(2))

g = lambda x: x**2
print(g(5))


def make_incrementor(n):
    return lambda x: x + n
print(make_incrementor(2)(8))


