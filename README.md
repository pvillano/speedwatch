# speedwatch
A Python utility for Project Euler Solving

Speedwatch is a utility for checking the correctness and estimating the run time of a ProjectEuler solution. Given a function and a list of inputs, it extrapolates how long the last input will take, using a list of big O functions. Big O functions that grow faster than the runtime of solver will overestimate the final amount of time, and functions that grow slower than the runtime of solver will underestimate, but both will converge to the actual runtime.

## Usage
**watch_time**(solver, test_inputs, **[**last, big_o_funcs=(linear, nlog2n, square, cube, exp)**]**)
* **solver** - A function that operates on the elements of test_inputs
* **test_inputs** - A sequence of numerical inputs to solver
* **last** - The final input to solver,  used to calculate the expected total time. Defaults to last element of test_inputs
* **big_o_funcs** - A Sequence of functions that model different growth rates. Defaults to a list of common big O functions.

## Examples
### Minimum Inputs
Let's see what happens when we run the following code:
```python
def sum_squares(n):
    return sum(i ** 2 for i in range(n))

watch_time(sum_squares, [10000, 100000, 1000000, 10000000, 100000000])
```
Output:
```
linear nlog2n square   cube    exp | curr   sum_squares(100000000)= ?
   50s     2m     6d   159y    inf |    5ms sum_squares(10000)= 333283335000
   47s     1m    13h     1y    inf |   47ms sum_squares(100000)= 333328333350000
   54s     1m     1h     6d    inf |  540ms sum_squares(1000000)= 333332833333500000
   48s    55s     8m     1h    inf |     5s sum_squares(10000000)= 333333283333335000000
```
From this we can determine that sum_squares is a little faster than linear and predict that sum_squares(1000000000) will take around around 48 seconds.
```
calculating final answer...
48s    sum_squares(100000000)= 333333328333333350000000
```
### Advanced inputs
Let's try the computer science favorite, recursive fibonacci, with custom big O functions
```python
from speedwatch import cube, exp

def golden(n):
    return 1.6 ** n
    
problem_sizes = range(30, 40)
big_o_funcs=[cube, golden, exp]

watch_time(fibonacci, problem_sizes, 50, big_o_funcs)
```
Output:
```
  cube golden    exp | curr   fibonacci(50)= ?
    2s     2h     7d | 537ms  fibonacci(30)= 1346269
    4s     2h     5d | 836ms  fibonacci(31)= 2178309
    5s     2h     4d | 1s     fibonacci(32)= 3524578
    8s     2h     3d | 2s     fibonacci(33)= 5702887
   13s     2h     3d | 4s     fibonacci(34)= 9227465
   18s     2h     2d | 6s     fibonacci(35)= 14930352
   25s     2h     2d | 9s     fibonacci(36)= 24157817
   37s     2h     1d | 15s    fibonacci(37)= 39088169
   55s     2h     1d | 24s    fibonacci(38)= 63245986
    2m     2h     1d | 43s    fibonacci(39)= 102334155
calculating final answer...   
```
It looks like fibonacci is almost exacly O(golden) time. It's going to take around two hours to compute!

# Todo
- [x] Make something that I will use
- [x] Human readable time formatting
- [ ] Command line interface
- [ ] Support function names longer than 6 characters
- [ ] Decimals for times near 1





