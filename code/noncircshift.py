# Utility function
# Shift an array in 2D
# Examples:
# B = noncircshift(A,[0 1]) > Right
# noncircshift(A,[0 -1]) > Left
# noncircshift(A,[1 1]) > Right Down
#

import numpy as np


def noncircshift(A, offsets):
    offsets = np.negative(offsets)
    siz = np.shape(A)
    N = len(siz)
    if len(offsets) < N:
        offsets.extend([0] * (N - len(offsets)))
    B = np.zeros(siz)
    indices = []
    for i in range(N):
        idx = np.arange(siz[i]) + offsets[i]
        idx = np.clip(idx, 0, siz[i] - 1)  # 确保索引值在有效范围内
        indices.append(idx)
    src_indices = np.meshgrid(*indices, indexing="ij")
    dest_indices = np.meshgrid(
        *[idx - off for idx, off in zip(indices, offsets)], indexing="ij"
    )
    B[tuple(dest_indices)] = A[tuple(src_indices)]
    return B, src_indices, dest_indices


# Example usage
if __name__ == "__main__":
    A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    offsets = [0, 1]
    B, src_indices, dest_indices = noncircshift(A, offsets)
    print("Shifted array:")
    print(B)
    print("Source indices:")
    print(src_indices)
    print("Destination indices:")
    print(dest_indices)
