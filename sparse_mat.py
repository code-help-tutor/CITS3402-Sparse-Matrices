WeChat: cstutorcs
QQ: 749389476
Email: tutorcs@163.com
import numpy as np
import time

# Sparse matrix classes
class COOMatrix:
    def __init__(self):
        self.data = []

    def add_element(self, i, j, val):
        self.data.append((i, j, val))

class CSRMatrix:
    def __init__(self):
        self.NNZ = []
        self.IA = []
        self.JA = []

    def convert_from_dense(self, dense_matrix):
        n_rows, n_cols = dense_matrix.shape
        self.IA.append(0)
        for i in range(n_rows):
            count = 0
            for j in range(n_cols):
                if dense_matrix[i, j]!= 0:
                    self.NNZ.append(dense_matrix[i, j])
                    self.JA.append(j)
                    count += 1
            self.IA.append(self.IA[-1] + count)

class CSCMatrix:
    def __init__(self):
        self.NNZ = []
        self.IA = []
        self.JA = []

    def convert_from_dense(self, dense_matrix):
        n_rows, n_cols = dense_matrix.shape
        self.IA.append(0)
        for j in range(n_cols):
            count = 0
            for i in range(n_rows):
                if dense_matrix[i, j]!= 0:
                    self.NNZ.append(dense_matrix[i, j])
                    self.JA.append(i)
                    count += 1
            self.IA.append(self.IA[-1] + count)

# Matrix operations
def scalar_multiplication(matrix, scalar):
    result = np.zeros(matrix.shape, dtype=matrix.dtype)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            result[i, j] = matrix[i, j] * scalar
    return result

def trace(matrix):
    if matrix.shape[0]!= matrix.shape[1]:
        raise ValueError("Trace is only defined for square matrices.")
    trace_value = 0
    for i in range(matrix.shape[0]):
        trace_value += matrix[i, i]
    return trace_value

def matrix_addition(matrix1, matrix2):
    if matrix1.shape!= matrix2.shape:
        raise ValueError("Matrices must have the same dimensions for addition.")
    result = np.zeros(matrix1.shape, dtype=matrix1.dtype)
    for i in range(matrix1.shape[0]):
        for j in range(matrix1.shape[1]):
            result[i, j] = matrix1[i, j] + matrix2[i, j]
    return result

def transpose(matrix):
    result = np.zeros((matrix.shape[1], matrix.shape[0]), dtype=matrix.dtype)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            result[j, i] = matrix[i, j]
    return result

def matrix_multiplication(matrix1, matrix2):
    if matrix1.shape[1]!= matrix2.shape[0]:
        raise ValueError("Matrices have incompatible dimensions for multiplication.")
    result = np.zeros((matrix1.shape[0], matrix2.shape[1]), dtype=matrix1.dtype)
    for i in range(matrix1.shape[0]):
        for j in range(matrix2.shape[1]):
            for k in range(matrix1.shape[1]):
                result[i, j] += matrix1[i, k] * matrix2[k, j]
    return result

# File reading function
def read_matrix_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        data_type = lines[0].strip().split()[0]
        n_rows, n_cols = map(int, lines[1].strip().split())
        matrix = np.zeros((n_rows, n_cols), dtype=np.float64 if data_type == 'float' else np.int64)
        for i, line in enumerate(lines[2:]):
            values = list(map(float, line.strip().split()))
            for j, value in enumerate(values):
                matrix[i, j] = value
    return matrix

# Main function
def main():
    import sys

    # Parse command-line arguments
    if len(sys.argv) < 4:
        print("Usage: python program.py <operation> -f <matrix_file1> [<matrix_file2>]")
        sys.exit(1)

    operation = sys.argv[1]
    matrix_files = sys.argv[3].split()

    # Read matrices from files
    matrices = []
    for file in matrix_files:
        matrices.append(read_matrix_file(file))

    # Convert matrices to sparse format (CSR in this example)
    sparse_matrices = []
    for matrix in matrices:
        sparse_matrix = CSRMatrix()
        sparse_matrix.convert_from_dense(matrix)
        sparse_matrices.append(sparse_matrix)

    # Perform the requested operation
    start_time = time.time()
    if operation == '-sm':
        scalar = float(sys.argv[2])
        result = scalar_multiplication(matrices[0], scalar)
    elif operation == '-tr':
        result = trace(matrices[0])
    elif operation == '-ad':
        result = matrix_addition(matrices[0], matrices[1])
    elif operation == '-ts':
        result = transpose(matrices[0])
    elif operation == '-mm':
        result = matrix_multiplication(matrices[0], matrices[1])
    else:
        print("Invalid operation.")
        sys.exit(1)
    end_time = time.time()

    # Log the results
    output_file = f"{time.strftime('%Y%m%d_%H%M%S')}_{operation}.out"
    with open(output_file, 'w') as file:
        file.write(f"Operation: {operation}\n")
        file.write(f"File1: {matrix_files[0]}\n")
        if len(matrix_files) > 1:
            file.write(f"File2: {matrix_files[1]}\n")
        file.write(f"Time: {end_time - start_time:.6f} seconds\n")
        if operation!= '-tr':
            file.write(f"Result:\n{np.array_str(result, precision=2)}\n")
        else:
            file.write(f"Result: {result}\n")

if __name__ == '__main__':
    main()
