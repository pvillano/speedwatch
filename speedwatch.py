from math import log2
from math import log10
from math import inf
from math import e
from math import pi
import re
import time
import sys


def linear(n):
    return n


def nlog2n(n):
    if n > sys.float_info.max ** (1 / 2.0): return inf
    return n * log2(n)


def square(n):
    return n * n


def cube(n):
    if n > sys.float_info.max ** (1 / 3.0): return inf
    return n ** 3


def exp(n):
    if n > 1023: return inf
    return 2.0 ** n


def fact(n):
    n = float(n)
    if n > 170: return inf
    return ((2.0 * pi * n) ** 0.5) * ((n / e) ** n)


def log2fact(n):
    return 0.5 * log2(2 * pi * n) + n * log2(n) - n * log2(e)


def wordtime(t):
    if t == 0: return "0s"
    if t < .001:
        return re.sub('\+0', '', "{:.0e}ns".format(t * (10 ** 9)))
    if t < 1: return "{:.0f}ms".format(t * 1000)
    if t < 60: return "{:.0f}s".format(t)
    t /= 60
    if t < 60: return "{:.0f}m".format(t)
    t /= 60
    if t < 24: return "{:.0f}h".format(t)
    t /= 24
    if t < 7: return "{:.0f}d".format(t)
    # if t < 30.4: return "{:.0f}w".format(t / 7)
    if t < 365.2425: return "{:.0f}M".format(t / 30.4)
    t /= 365.2425
    if t < 1000: return "{:.0f}y".format(t)
    if log10(t) < 1000: return re.sub('\+0*', '', "{:.0e}y".format(t))
    return "inf"


def log2fun(function):
    if function == fact:
        return log2fact
    elif function == exp:
        return linear
    return None


def safediv(algorithm, num, denom, log2max):
    logfun = log2fun(algorithm)
    if logfun is None:
        return algorithm(num) / max(algorithm(denom), 1)
    if logfun(num) - logfun(denom) > log2max:
        return inf
    else:
        return 2.0 ** (logfun(num) - logfun(denom))


def watch_time(solver, test_inputs, last=None, big_o_funcs=(linear, nlog2n, square, cube, exp)):
    """

    This is a utility for checking the correctness and estimating the run time of a ProjectEuler solution. It works by
    timing solver on each input in test_inputs, and extrapolating how long the last problem will take using the big o
    functions. The values of test_inputs should be proportional to the size of the input.
    Big o functions that grow faster than the runtime of solver will overestimate the final amount of time,
    and functions that grow slower than the runtime of solver will underestimate, but both will converge to the actual
    runtime of last.

    :param solver: a function that takes integer inputs
    :param test_inputs: a list of valid numerical inputs for the solver
    :param last: the final input for the solver. If none, the last value in test_inputs is used
    :param big_o_funcs: a list of int -> float algorithms to use for estimating the amount of time the final calculation
    will take
    """

    if last is None:
        last = test_inputs[-1]
        test_inputs = test_inputs[:-1]

    for algorithm in big_o_funcs:
        print("{:>6}".format(algorithm.__name__), end=" ")
    print("| curr   {}({})= ?".format(solver.__name__, last))
    for size in test_inputs:

        start = time.time()
        answer = solver(size)
        stop = time.time()
        delta = stop - start

        for algorithm in big_o_funcs:
            log2max = log2(sys.float_info.max) - log2(max(delta, 1))
            eta = delta * safediv(algorithm, last, size, log2max)
            print("{:>6}".format(wordtime(eta)), end=' ')

        print("| {:>6} {}({})= {}".format(wordtime(delta), solver.__name__, size, answer))

    print("calculating final answer...")

    start = time.time()
    answer = solver(last)
    stop = time.time()
    delta = stop - start

    print("{:6} {}({})= {}".format(wordtime(delta), solver.__name__, last, answer))
