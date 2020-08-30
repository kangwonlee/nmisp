import numpy as np


def inv(A:np.ndarray, b_verbose:bool=True) -> np.ndarray:
    return elimination(
        np.array(
            np.hstack(
                [A, np.identity(A.shape[0])]
            )
        )*1.0,
        b_verbose=b_verbose,
    )


def elimination(AX:np.ndarray, b_verbose:bool=True) -> np.ndarray:
    # pivot loop
    for p in range(AX.shape[0]):

        if b_verbose:
            print(f"Row {p+1} is now the Pivot Row.")
        
        one_over_pivot = 1.0 / AX[p, p]

        if abs(1 - one_over_pivot) > np.finfo(np.float32).eps:
            if b_verbose:
                print(f"Normalize Row {p+1} with {one_over_pivot}.")

            # normalize the pivot row
            for j in range(AX.shape[1]):
                AX[p, j] *= one_over_pivot

            if b_verbose:
                print(AX)

        # row loop
        for i in range(AX.shape[0]):
            if i != p and (abs(AX[i, p]) > np.finfo(np.float32).eps):
                # row operation
                multiplier = - AX[i, p]
                
                if b_verbose:
                    print(f"Row {i+1} += ({multiplier}) x Row {p+1}")
                
                AX[i, :] += multiplier * AX[p, :]
                
                if b_verbose:
                    print(AX)

    return AX[:, AX.shape[0]:]

