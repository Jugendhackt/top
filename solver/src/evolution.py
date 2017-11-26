from generator import generate, mutate
from benchmark import benchmark


def do_evoluton(constraints, n=1000):
    solutions = [generate(constraints) for _ in range(100)]

    for _ in range(n):
        solutions = sorted(solutions, key=benchmark)
        solutions[50:] = solutions[:50]
        solutions[50:] = [mutate(x) for x in solutions]

    return max(solutions, key=benchmark)
