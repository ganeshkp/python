# https://python-course.eu/advanced-python/recursive-functions.php

def factorial(n):
    print("factorial has been called with n = " + str(n))
    if n == 1:
        return 1
    else:
        res = n * factorial(n-1)
        print("intermediate result for ", n, " * factorial(", n-1, "): ", res)
        return res


# print(factorial(5))
# -----------------------------------------------------------------------------


""" A module containing both a recursive and an iterative implementation of the Fibonacci function. 
The purpose of this module consists in showing the inefficiency of a purely recursive implementation of Fibonacci! """


def fib(n):
    """ recursive version of the Fibonacci function """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def fibi(n):
    """ iterative version of the Fibonacci function """
    old, new = 0, 1
    if n == 0:
        return 0
    for i in range(n-1):
        old, new = new, old + new
    return new


memo = {0: 0, 1: 1}


def fibm(n):
    """ recursive Fibonacci function which memoizes previously 
    calculated values with the help of a dictionary memo"""
    if not n in memo:
        memo[n] = fibm(n-1) + fibm(n-2)
    return memo[n]


print(fib(10))

# ---------------------------------------------------------------


class kFibonacci:

    def __init__(self, k, initials, coefficients):
        self.memo = dict(zip(range(k), initials))
        self.coeffs = coefficients
        self.k = k

    def __call__(self, n):
        k = self.k
        if n not in self.memo:
            result = 0
            for coeff, i in zip(self.coeffs, range(1, k+1)):
                result += coeff * self.__call__(n-i)
            self.memo[n] = result
        return self.memo[n]


fib = kFibonacci(2, (0, 1), (1, 1))
lucas = kFibonacci(2, (2, 1), (1, 1))

for i in range(1, 16):
    print(i, fib(i), lucas(i))
