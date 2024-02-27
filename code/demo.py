import numpy as np
p = 0.5  # 非零元素的比例
position = np.random.rand(20, 2)
position = np.array(position >= p, dtype=int)
print(position)
