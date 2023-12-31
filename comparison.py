"""
Below is the 24-solver algorithm from the Github repository https://github.com/BGR360/TwentyFourSolver/tree/master

Specifically, everything below this string is copy-pasted from the one of the repository's python files,
https://github.com/BGR360/TwentyFourSolver/blob/master/my_algorithm.py

An extremely few very minor trivial changes were made to the copy-pasted raw code in order to get it to run locally.

This solver fails as it is unable to fully account for the grouping of terms together. For example, the very first
test I ran is [9,4,1,1], which is solvable if you group 9 and 1 as 9-1=8, and group 4 and 1 as 4-1=3, to have 
8*3=24. However, this solver says that there is no solution to [9,4,1,1]. 

From more empirical testing, it seems that this solver fails when more than one "bracket" is needed. Aka, grouping of
numbers is needed more than once. Perhaps this solver is intended to work for 24 under a different set of rules.
"""


"""
This is my custom algorithm for finding a solution to a 24 Card (or to any card).
Hopefully it should be smarter than the brute-force algorithm.


Theory behind the algorithm:

When humans try to solve a 24 Card, they don't think in a brute-force way. Humans are smart.
When I try to solve a 24 Card, I think of FACTORS. Factors are very important. Normally, I'll try to find a factor
of 24 on my card and see if I can arrange the other 3 numbers to make the other factor (e.g. my card has a 4 in
it, can I use the other 3 numbers to make 4 so that I can multiply 4 * 6?).


Generalizing:

I figured that I could make this algorithm recursive. What I imagined was this: I'd pick one number from the
card, and then see if the other 3 numbers can make the other number that I need. What this inherently necessitates is
a general function which can answer this question:
        > Given n numbers, can you use arithmetic to arrive at an answer x?

Or more programmatically written as:
        > solution(array, x)    # array has size n


My algorithm in a nutshell:

Given n numbers (stored in array A), can you use arithmetic to arrive at x?

1.  If n = 1:
    a)  If A[0] = x, then yes
    b)  If A[0] != x, then no

2.  If n = 2:
    a)  Try multiplying the two numbers
    b)  Try adding the two numbers
    c)  If x >= 0
        i)  Try subtracting the smaller from the larger
        ii) Else try subtracting the larger from the smaller
    d)  Try dividing the larger by the smaller
    e)  If any of those work, then yes. If not, then no solution.

3.  Try adding all the numbers in A together.

4.  Try multiplying all the numbers in A together.

5.  If there are factors of x in A, pick one.
    * Prefer 1 as a factor of x, and then prefer smaller factors
    a)  See if the other n - 1 numbers can make the other factor of x
        i)  If so, then yes
        ii) If not, then pick another factor

6.  If there are no more factors of x in A, then for each number a in A:
    a)  SUBTRACT a from x
    * Prefer even numbers
    b)  See if the other n - 1 numbers can form the result
        i)  If so, then yes
        ii) If not, try the next number

7.  If that fails, then for each number a in A:
    a)  ADD a to x
    * Prefer Even Numbers
    b)  See if the other n - 1 numbers can form the result
        i)  If so, then yes
        ii) If not, try the next number

8.  If that fails, then for each number a in A:
    a)  MULTIPLY x by a
    * Prefer smaller numbers
    b)  See if the other n - 1 numbers can form the result
        i)  If so, then yes
        ii) If not, then no solution
"""

import sys
from functools import reduce
from math import sqrt

class Operator(object):
    """
    Represents an operator ('*', '+', '-', '/') used in solving a 24 Card.
    """
    def __init__(self, op):
        self.op = op

    def evaluate(self, left, right):
        """
        Evaluates the result of multiplying/adding/subtracting/dividing left and right
        :param left: The left operand
        :param right: The right operand
        :return: The result of executing the operator on the two operands
        """
        if self.op == '*':
            return left * right
        elif self.op == '+':
            return left + right
        elif self.op == '-':
            return left - right
        elif self.op == '/':
            return float(left) / right
        else:
            return "Error"

    def __repr__(self):
        return str(self.op)

class Solution(object):
    """
    Represents a potential solution to a 24 Card.
    Has an array of 4 numbers and an array of 3 operations.
    A Solution does not necessarily have to be correct.
    """
    numbers = []
    operations = []

    def __init__(self):
        pass

    def evaluate(self):
        """
        Evaluates the result of this Solution.
        Executes the 3 operations (in order) on the 4 numbers (in order).
        num1 <op1> num2 <op2> num3 <op3> num4
        :return: The result of evaluating the Solution.
        """
        result = self.numbers[0]
        for i in range(1, len(self.numbers)):
            left = result
            right = self.numbers[i]
            operator = self.operations[i - 1]
            result = operator.evaluate(left, right)
        return result

    def __repr__(self):
        """
        Makes a human-readable string to represent this Solution
        :return The string representation of this Solution
        """
        result = str(self.numbers[0])
        for i in range(1, len(self.numbers)):
            op = self.operations[i - 1].op
            num = self.numbers[i]
            result += " " + op + " " + str(num)
        return result


# Constants for the different Operators
MUL = Operator('*')
ADD = Operator('+')
SUB = Operator('-')
DIV = Operator('/')
OPS = [MUL, ADD, SUB, DIV]

# The number of different combinations we've tried to find the answer
num_attempts = 0
current_attempt = Solution()
final_solution = None


def is_numeric(string):
    """
    Checks if a string is numeric (as in alphanumeric without the alpha)
    :param string: The string we want to check
    :return: True if the string is numeric, False if not
    """
    return string.isalnum() and not string.isalpha()

def get_factors(n):
    """
    Returns all the factors of n.
    Code for this method can be attributed to user agf on StackExchange
    :param n: An integer
    :return: A list of whole-number factors of n
    """
    return list(set(reduce(list.__add__, ([i, n//i] for i in range(1, int(sqrt(n)) + 1) if n % i == 0))))

def exclude(lst, value):
    """
    Returns lst excluding the first occurrence of value. Performs a deep copy in doing so.
    This is useful when we want to pass the n - 1 "other" numbers to another recursion of our solve() method.
    :param lst: The list we want to exclude value from
    :param value: The value we want to exclude
    :return: lst with the first occurrence of value excluded from it.
    """
    other_lst = lst[:]  # Perform a deep copy so we can safely modify it
    other_lst.remove(value)
    return other_lst

def sort_evens_first(lst):
    """
    Sorts a list, putting the even numbers first (in ascending order)
    :param lst: The list we want to sort
    :return: The sorted list
    """
    lst.sort()
    evens = []
    odds = []
    for num in lst:
        if num % 2 == 0:
            evens.append(num)
        else:
            odds.append(num)
    return evens + odds


def is_correct(solution, value=24):
    """
    Checks if solution evaluates to value
    :param solution: The Solution instance that should be checked
    :param value: The number that we expect solution to evaluate to
    :return: True if solution evaluates to value, False if otherwise
    """
    return solution.evaluate() == value


def solve(numbers, value):
    """
    Uses arithmetic (*, +, -, /) to arrive at value, using my custom recursive algorithm
    :param numbers: The list of numbers we're going to use to arrive at value
    :param value: The value that we want to arrive at using all of the
    :return: If solvable, returns a Solution instance. If not, returns False.
    """
    # Referring to the global variables we want to modify
    global num_attempts
    global current_attempt

    # Begin my algorithm
    solution = Solution()
    n = len(numbers)

    # print "Solve %s for %s" % (numbers, value)

    # 1. If n = 1
    if n < 1:
        return False
    if n == 1:
        num_attempts += 1
        if numbers[0] == value:
            solution.numbers = [value]
            solution.operations = []
            return solution
        else:
            return False

    # 2.  If n = 2:
    if n == 2:
        # a)  Try multiplying the two numbers
        num_attempts += 1
        if numbers[0] * numbers[1] == value:
            solution.numbers = numbers
            solution.operations = [MUL]
            return solution

        # b)  Try adding the two numbers
        num_attempts += 1
        if numbers[0] + numbers[1] == value:
            solution.numbers = numbers
            solution.operations = [ADD]
            return solution

        # Find the larger and the smaller number of the two
        smaller = numbers[0]
        larger = numbers[1]
        if smaller > larger:
            smaller = numbers[1]
            larger = numbers[0]

        # c)  If x >= 0
        if value >= 0:
            # i)  Try subtracting the smaller from the larger
            num_attempts += 1
            if larger - smaller == value:
                solution.numbers = [larger, smaller]
                solution.operations = [SUB]
                return solution
        else:
            # ii) Else try subtracting the larger from the smaller
            num_attempts += 1
            if smaller - larger == value:
                solution.numbers = [smaller, larger]
                solution.operations = [SUB]
                return solution

        # d)  Try dividing the larger by the smaller
        num_attempts += 1
        if float(larger) / smaller == value:
            solution.numbers = [larger, smaller]
            solution.operations = [DIV]
            return solution

        # e)  If any of those work, then yes. If not, then no solution.
        return False

    # 3.  Try adding all the numbers together.
    num_attempts += 1
    if sum(numbers) == value:
        solution.numbers = numbers
        for i in range(n - 1):
            solution.operations.append(ADD)
        return solution

    # 4.  Try multiplying all the numbers together.
    num_attempts += 1
    product = 1
    for num in numbers:
        product *= num
    if product == value:
        solution.numbers = numbers
        for i in range(n - 1):
            solution.operations.append(MUL)
        return solution


    # 5.  If there are factors of value in numbers, pick one.

    # Find the factors
    if value > 0:
        factors = get_factors(value)
        factors_in_list = []
        for num in numbers:
            if num in factors and num not in factors_in_list:
                factors_in_list.append(num)

        # Prefer smaller factors
        factors_in_list.sort()

        # Make an attempt for each factor in the list
        for factor in factors_in_list:
            other_factor = value / factor
            # See if the other n - 1 numbers can arrive at the other_factor
            other_numbers = exclude(numbers, factor)
            solution = solve(other_numbers, other_factor)
            # If so, append a '*' operation to the end of the solution
            if solution:
                solution.numbers.append(factor)
                solution.operations.append(MUL)
                return solution


    # 6.  Try subtracting from value
    # Try it for each number in numbers
    # Prefer even numbers
    numbers_evens_first = sort_evens_first(numbers)
    for num in numbers_evens_first:
        result = value - num
        # See if the other n - 1 numbers can arrive at the result
        other_numbers = exclude(numbers, num)
        solution = solve(other_numbers, result)
        # If so, append a '+' operation to the end of the solution
        if solution:
            solution.numbers.append(num)
            solution.operations.append(ADD)
            return solution

    # 7.  Try adding to value
    # Try it for each number in numbers
    # Prefer even numbers
    for num in numbers_evens_first:
        result = value + num
        # See if the other n - 1 numbers can arrive at the result
        other_numbers = exclude(numbers, num)
        solution = solve(other_numbers, result)
        # If so, append a '+' operation to the end of the solution
        if solution:
            solution.numbers.append(num)
            solution.operations.append(SUB)
            return solution

    # 8.  Try multiplying value
    # Try it for each number in numbers
    # Prefer smaller numbers
    numbers.sort()
    for num in numbers:
        result = value * num
        # See if the other n - 1 numbers can arrive at the result
        other_numbers = exclude(numbers, num)
        solution = solve(other_numbers, result)
        # If so, append a '/' operation to the end of the solution
        if solution:
            solution.numbers.append(num)
            solution.operations.append(DIV)
            return solution

    return False


def solve_card(card):
    """
    This method solves the 24 Card using my custom algorithm
    :param card: A list representing the 24 Card
    :return: Returns a Solution instance if a solution was found, and False if no solution was found.
    """
    return solve(card, 24)


# The 24 card. It's an array of 4 numbers
card = [10,3,10,9]

# Get the card's numbers from the user
"""
if len(sys.argv) <= 1:
    user_input = raw_input("Please enter 4 numbers separated by a space: ")
    split_input = user_input.split()
    for num_str in split_input:
        card.append(int(num_str))
else:
    for arg in sys.argv[1:]:
        if is_numeric(arg):
            card.append(int(arg))
"""

# Solve the card
solution = solve_card(card)

# Print results
if solution:
    print (f"Solution: {solution}")
else:
    print ("No solution found.")

print (f"Number of attempts: {num_attempts}")