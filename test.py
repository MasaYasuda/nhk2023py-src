import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def f(a, m, r):
    return (a * m + (1 - a) * r) / (m + r)

a = np.linspace(0, 1, 100)
m = np.linspace(0, 100, 100)
r = np.linspace(0, 100, 100)

A, M, R = np.meshgrid(a, m, r)
F = f(A, M, R)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(A, M, F, cmap='viridis')

ax.set_xlabel('a')
ax.set_ylabel('m')
ax.set_zlabel('f(a, m, r)')

plt.show()
