# Berkowitz
**berkowitz** is a pure Python implementation of Samuelson–Berkowitz algorithm for computing characteristic polynomial of an $n×n$ matrix.

---

## ⚠️ Disclaimer

This project is part of ongoing research and may evolve as the work progresses. Interfaces and functionality are subject to change without notice. Use with caution in production or critical systems.

## 📘 Samuelson–Berkowitz algorithm
Samuelson–Berkowitz algorithm provides a fast and efficient method for computing the **characteristic polynomial** of a square matrix $A$ of size $n×n$. The characteristic polynomial $p(λ)$ is given by:

$$
p(λ) = \det(λI − A)
$$

where $λ$ is a variable and $I$ is the identity matrix. Traditionally, calculating the characteristic polynomial involves computing a determinant, which can be computationally expensive. Berkowitz’s algorithm, however, avoids direct determinant computation, instead constructing **Toeplitz matrices** that help iteratively determine the polynomial's coefficients. These matrices have the form:

$$
T_n = \begin{bmatrix}1 & 0 & 0 & ... & 0 \\\ a_{11} & 1 & 0 & ... & 0 \\\ -RC & a_{11} & 1 & ... & 0 \\\ -RA_1C & -RC & a_{11} & ... & 0 \\\ \vdots & \vdots & \vdots & \vdots & 0\end{bmatrix}
$$

where $R$, $C$ and $A_1$ are vectors or matrices derived from the original matrix $A$. The algorithm starts with an initial characteristic vector and iteratively computes the next vectors using matrix multiplication.

Unlike many traditional methods, which involve division operations during the determinant calculation, **Berkowitz's algorithm is division-free**. It relies entirely on matrix multiplication and subtraction. This is crucial for numerical stability and efficiency, especially for large matrices or matrices with ill-conditioned elements, where divisions can lead to **precision errors**. Division operations in numerical computations are prone to rounding errors, which can accumulate and degrade the accuracy of the result. By avoiding division, Berkowitz's method ensures more stable and reliable results.

One of the significant advantages of Berkowitz's algorithm is its parallelization potential. Since each step in the recursive computation involves matrix multiplications that are independent of each other, the algorithm is highly suitable for parallel execution. The parallelism allows Berkowitz’s method to scale efficiently for large matrix sizes, making it an attractive choice for high-performance computing scenarios.

## 💻 Implementation
This repository contains a **pure Python implementation** of the Samuelson–Berkowitz algorithm. The code aims to provide a **reference implementation** that is simple, clear and easy to follow. The code makes extensive use of Python's type hints to provide clear and maintainable code. The type annotations are checked using [MyPy](https://mypy-lang.org/), ensuring that the code adheres to its declared types and minimizes the risk of runtime errors.

This implementation is **not optimized for maximum performance** but serves as a **reference implementation** for those who wish to understand the inner workings of Berkowitz's algorithm.

### 🚀 Parallelization Support

One of the key advantages of the Berkowitz algorithm is its potential for **parallelization**. Since the intermediate steps of the algorithm involve independent matrix multiplications, the computations can be performed in parallel, making the algorithm particularly suitable for larger matrices or high-performance environments.

The parallelization is implemented using Python’s `concurrent.futures` module, which provides support for executing tasks asynchronously in threads, processes or sub-interpreters (starting from Python 3.14). The implementation includes the following parallelization options:

1. Thread Pool:
   * Uses Python's `ThreadPoolExecutor` to run tasks concurrently in separate threads.
   * Suitable for smaller matrices or I/O-bound operations, as it avoids the overhead of process creation.

2. Process Pool:
   * Uses `ProcessPoolExecutor` to run tasks in separate processes.
   * Ideal for CPU-bound operations where the Global Interpreter Lock (GIL) might limit performance in a multithreaded environment.

3. Interpreter Pool (requires Python >= 3.14):
   * This option leverages multiple Python interpreters to bypass the GIL and achieve parallelism across multiple CPU cores.

The parallelization support makes it easy to scale the algorithm depending on hardware, with the ability to adjust the number of workers and choose the appropriate worker type for a use case.

**Note:** The algorithm’s parallelization is optional and controlled through the `workers` and `worker_class` parameters, allowing users to select the best configuration based on the matrix size and available system resources.

### ✅ Correctness & Testing
The core algorithm has been validated against a known, high-quality implementation from the [SymPy](https://www.sympy.org/) library, which is widely used in mathematical and symbolic computation. Extensive tests are included to ensure the correctness of the results for both **numeric** and **symbolic** matrices. The test suite covers various scenarios, including edge cases such as small matrices (1x1 or 2x2), large matrices, random matrices with random coefficients and symbolic matrices with polynomial entries. This ensures that the algorithm works correctly across a wide range of inputs.

## 📦 Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/vladimir-poghosyan/Berkowitz.git
cd Berkowitz
python3 -m pip install .
```

## 🛠️ Usage Example
```Python
from berkowitz import berkowitz


print(berkowitz([[3, 5], [7, 9]]))  # prints ((1,), (1, -3), (1, -12, -8))
print(berkowitz([[3, 5], [7, 9]], workers=4, worker_class='process'))  # parallel version of the same call
```

In the output of the above code each tuple represents an intermediate vector of characteristic polynomial coefficients computed at successive stages of the algorithm.

## 📚 References
1. **Berkowitz S. J.**. *On computing the determinant in small parallel time using a small number of processors.* Information Processing Letters, 18(3):147–150, 1984.
2. **Abdeljaoued J.**. *The Berkowitz algorithm, Maple and computing the characteristic polynomial in an arbitrary commutative ring.* MapleTech Vol. 4(3):21-32, 1997.
3. **Michael Soltys**. *Berkowitz's Algorithm and Clow Sequences.* The Electronic Journal of Linear Algebra, 9:42-54, 2002.

## 📄 License

This project is licensed under the MIT License. See LICENSE for details.
