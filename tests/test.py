import unittest

from random import randint
from sys import version_info

import sympy

from berkowitz import berkowitz


class TestBerkowitz(unittest.TestCase):

    MAX_WORKERS: int = 4
    SUB_INTERPRETERS_AVAILABLE: bool = version_info.minor > 13

    def test_numeric_matrix(self) -> None:
        for n in range(101):
            matrix = [
                [randint(-10000, 10000) for j in range(n)]
                for i in range(n)
            ]
            berkowitz_vectors = berkowitz(matrix)

            assert berkowitz_vectors == sympy.Matrix(matrix).berkowitz()
            assert berkowitz_vectors == berkowitz(
                matrix,
                TestBerkowitz.MAX_WORKERS
            )
            assert berkowitz_vectors == berkowitz(
                matrix,
                TestBerkowitz.MAX_WORKERS,
                'process'
            )

            if TestBerkowitz.SUB_INTERPRETERS_AVAILABLE:
                assert berkowitz_vectors == berkowitz(
                    matrix,
                    TestBerkowitz.MAX_WORKERS,
                    'interpreter'
                )

    def test_symbolic_matrix(self) -> None:
        matrices: tuple = (
            [
                ["1 - t", "t ^ 2"],
                ["t + 6", "2 + t ^ 2"]
            ],
            [
                ["1 - t", "1 + 2 * t", "2 + 3 * t", 1],
                ["t", "1 - t", "t ^ 2", "t"],
                ["t ^ 3", "t + 6", "2 + t ^ 2", "2 - t"],
                ["1 - t", "1 + 2 * t ^ 2", "2 + t", "1 - t"]
            ],
            [
                ["1 - t", "12 * t - 3", "t - t ^ 2", "6 + 7 * t", "12 - t",
                 "t", "1 + t"],
                ["t ^ 2", 6, "9 * t", "11 * t ^ 2", "7 * t + 2", "t + 3",
                 "t ^ 2"],
                ["2 * t", "7 + t ^ 2", "12 + 7 * t", 3, 24, "3 * t", "t + 2"],
                ["4 * t + t ^ 2", "t ^ 3 + 1", "t - 2", "2 * t ^ 2 + t ^ 3",
                 "t ^ 2 - t", "t ^ 2", "t - t ^ 2"],
                [3, "2 * t", "t ^ 2 - 2 * t", "t", "2 * t - 1", "2 * t",
                 "t ^ 3"],
                ["7 + t ^ 2", "8 * t + 1", 10, "30 - t", "t ^ 3", "6 - t ^ 2",
                 2],
                ["9 * t", "1 + t ^ 2", "4 * t", "1 + t ^ 2", "1 + t", "7 * t",
                 "7 + t ^ 2"]
            ],
            [
                ["x + y ^ 2 + 1", "x * y ^ 2 - 2 * x", 5, "x"],
                ["2 - x", "4 + 3 * x ^ 2", "7 * x * y", "y"],
                ["x", "y", "x * y", 1],
                [1, "x", "y", "x * y"]
            ],
            [
                ["3 * x - y ^ 2 + z", 0, "(2 * z - 4 * x) / (y - 4)", 6],
                [4, "(4 - x) ^ 2 + (3 + y) ^ 2", -1,
                 "5 * x * z - sqrt(1 - y)"],
                ["exp(x) / (1 - y + 2 * z)", "-2 ^ z", "log(x) + 2 ^ y", 0],
                ["(1 + z) ^ 2", "sin(2 * x) - y ^ 3", 2, "x ^ (1 - y)"]
            ],
        )

        for matrix in matrices:
            polynomial_matrix = [
                [sympy.sympify(item) for item in row]
                for row in matrix
            ]
            berkowitz_vectors = berkowitz(polynomial_matrix)

            assert berkowitz_vectors == sympy.Matrix(matrix).berkowitz()
            assert berkowitz_vectors == berkowitz(
                polynomial_matrix,
                TestBerkowitz.MAX_WORKERS
            )
            assert berkowitz_vectors == berkowitz(
                polynomial_matrix,
                TestBerkowitz.MAX_WORKERS,
                'process'
            )

            if TestBerkowitz.SUB_INTERPRETERS_AVAILABLE:
                assert berkowitz_vectors == berkowitz(
                    polynomial_matrix,
                    TestBerkowitz.MAX_WORKERS,
                    'interpreter'
                )


if __name__ == '__main__':
    unittest.main()
