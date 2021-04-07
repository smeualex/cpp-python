import os

def multiply(a, b):
    print(" > Python script: Will compute", a, "times", b)
    c = 0
    for i in range(0, a):
        c = c + b
    print(" > Python script: returning ", c)
    return c