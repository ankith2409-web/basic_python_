def multiply_matrices(A, B):
    """
    Multiplies two 2D matrices A and B.
    """
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError("Cannot multiply: columns of A must match rows of B.")

    # Initialize the result matrix with zeros
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    # Perform matrix multiplication
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result

def print_matrix(name, matrix):
    print(f"\nMatrix {name}:")
    for row in matrix:
        print(row)

def main():
    print("=== Simple Matrix Multiplication ===")
    
    # Define two 3x3 matrices
    A = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    B = [
        [9, 8, 7],
        [6, 5, 4],
        [3, 2, 1]
    ]

    print_matrix("A", A)
    print_matrix("B", B)

    try:
        C = multiply_matrices(A, B)
        print_matrix("A * B Result", C)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
