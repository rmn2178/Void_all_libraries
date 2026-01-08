import matplotlib.pyplot as plt
import numpy as np

# Create a figure
fig = plt.figure(figsize=(10, 7))

# Explicitly add a 3D subplot
ax = fig.add_subplot(111, projection='3d')

# 1. Prepare the data
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

# 2. Plot the surface with a colormap
surf = ax.plot_surface(X, Y, Z, cmap='viridis',edgecolor='none', antialiased=True)

# 3. Add a color bar
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

# 4. Labels and Title
ax.set_title('Basic 3D Surface Plot')
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')

plt.show()