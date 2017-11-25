# Solver
The Solver takes a simplified representation of the Problem and tries to find a good solution.
The "goodness" is defined by a cost function, that contains the tradeofft, we made in the importance
of different goals.

## Algorithms
Because the search space is very large, we can not do an exhaustive search of every combination
and sort them by the result of the cost function, we have to do something smarter. There are several
different approaches for solving such combinatorial optimisation problems:

