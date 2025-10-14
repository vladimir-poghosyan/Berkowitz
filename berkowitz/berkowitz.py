from concurrent.futures import (
    ProcessPoolExecutor,
    ThreadPoolExecutor,
    as_completed,
)

from typing import Final, Literal


type Number = int | float
type Matrix = list[list[Number]]


WORKER_CLASSES: Final[dict] = {
    'thread': ThreadPoolExecutor,
    'process': ProcessPoolExecutor,
}


def __mat_mul(a: Matrix, b: Matrix, sign: int = 1) -> Matrix:
    if len(a[0]) != len(b):
        raise ValueError('Matrix dimension mismatch for multiplication')

    b_t = list(zip(*b))  # transpose of matrix b

    return [
        [
            sum(sign * elem_a * elem_b for elem_a, elem_b in zip(row_a, col_b))
            for col_b in b_t
        ]
        for row_a in a
    ]


def __toeplitz_matrix(
    A: Matrix,
    n: int,
) -> Matrix:
    """ Compute Toeplitz matrix

    Parameters
    ----------
    A : Matrix
    n : int

    Returns
    -------
    Matrix

    """
    k: int = n - 1

    a: Number = -A[k][k]
    R: Matrix = [A[k][:k]]
    C: Matrix = [[A[i][k]] for i in range(0, k)]
    A = [A[i][:k] for i in range(0, k)]

    T: Matrix = [[0] * n for i in range(0, n + 1)]
    coeffs: list = [C]

    # -R(A₁^n)C
    for i in range(0, n - 2):
        coeffs.append(__mat_mul(A, coeffs[i]))
        coeffs[i] = __mat_mul(R, coeffs[i], -1)[0][0]

    # update the last appended vector
    coeffs[n - 2] = __mat_mul(R, coeffs[n - 2], -1)[0][0]
    coeffs = [1, a] + coeffs

    for i in range(n):
        for j, item in enumerate(coeffs[:n - i + 1]):
            T[j + i][i] = item

    return T


def berkowitz(
    matrix: Matrix,
    workers: int = 1,
    worker_class: Literal['thread', 'process'] = 'thread'
) -> tuple[tuple[Number]]:
    """Compute the characteristic polynomial of a square matrix using
    Berkowitz's algorithm.

    Returns a tuple of coefficient vectors representing the characteristic
    polynomial of the input matrix using Berkowitz's algorithm.

    Parameters
    ----------
    matrix : Matrix
    workers : int
        Number of parallel workers to use (defaults to 1)
    worker_class : Literal['thread', 'process']
        Type of workers to use, either threads or processes

    Returns
    -------
    tuple[tuple[Number]]

    """
    if not isinstance(matrix, list):
        raise ValueError('Invalid matrix provided')

    N: int = len(matrix)

    if any(len(row) != N for row in matrix):
        raise ValueError('Matrix must be square')

    if worker_class not in WORKER_CLASSES:
        raise ValueError(f'Invalid worker class "{worker_class}"')

    berk = ((1,),)

    if not matrix:
        return berk

    A = matrix
    transforms: list = [0] * (N - 1)

    """ Compute Toeplitz matrices

    | 1         | 0     | 0    | 0    | ... |
    | a₁,₁      | 1     | 0    | 0    | ... |
    | -RC       | a₁,₁  | 1    | 0    | ... |
    | -RA₁C     | -RC   | a₁,₁ | 1    | ... |
    | -R(A₁^2)C | -RA₁C | -RC  | a₁,₁ | ... |
    | ...       | ...   | ...  | ...  | ... |

    where

    | a₁,₁ | R  |
    | C    | A₁ |

    """
    if workers < 2:
        for n in range(N, 1, -1):
            transforms[n - 2] = __toeplitz_matrix(A, n)
    else:
        with WORKER_CLASSES[worker_class](max_workers=workers) as executor:
            for future in as_completed(
                executor.submit(__toeplitz_matrix, A, n)
                for n in range(N, 1, -1)
            ):
                T = future.result()
                transforms[len(T) - 3] = T

    # T₀T₁T₂...Tₙ₋₁ vector
    polys: list[list] = [[[1], [-A[0][0]]]]
    for T in transforms:
        polys.append(__mat_mul(T, polys[-1]))

    polys = [[item[0] for item in rec] for rec in polys]

    return berk + tuple(map(tuple, polys))
