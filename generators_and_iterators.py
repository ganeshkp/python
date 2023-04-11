# https://python-course.eu/advanced-python/generators-and-iterators.php
def count(firstval=0, step=1):
    x = firstval
    while True:
        yield x
        x += step


# counter = count()  # count will start with 0
# for i in range(10):
#     print(next(counter), end=", ")

# start_value = 2.1
# stop_value = 0.3
# print("\nNew counter:")
# counter = count(start_value, stop_value)
# for i in range(10):
#     new_value = next(counter)
#     print(f"{new_value:2.2f}", end=", ")

# ----------------------------------------------
# Fibonacci as a Generator:


def fibonacci(n):
    """ A generator for creating the Fibonacci numbers """
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n):
            return
        yield a
        a, b = b, a + b
        counter += 1


f = fibonacci(5)
for x in f:
    print(x, " ", end="")
print()
