import time
import numpy as np
from functools import wraps

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("total time:", end-start)
        return result
    return wrapper

def measure_time2(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    print("total time:", end-start)
    return result

@measure_time
def matrix_multiply(matrix1, matrix2):
    result = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]
    return result

@measure_time
def matrix_multiply_numpy(matrix1, matrix2):
    result = np.dot(matrix1, matrix2)
    return result

size = 10
matrix1 = [[np.random.rand() for _ in range(size)] for _ in range(size)]
matrix2 = [[np.random.rand() for _ in range(size)] for _ in range(size)]

matrix_multiply(matrix1, matrix2)

np_matrix1 = np.random.rand(size, size)
np_matrix2 = np.random.rand(size, size)

matrix_multiply_numpy(np_matrix1, np_matrix2)


# measure_time2(matrix_multiply, matrix1, matrix2)
# measure_time2(matrix_multiply_numpy, np_matrix1, np_matrix2)