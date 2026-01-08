import matplotlib.pyplot as plt
import numpy as np

# Set a style for a cleaner look
plt.style.use('seaborn-v0_8-darkgrid')

# 1. Generate synthetic data
n = 500
theta = np.linspace(0, 15 * np.pi, n)
z = np.linspace(-2, 2, n)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)

# Add some random noise to make it look like a real dataset
x += np.random.normal(0, 0.1, n)
y += np.random.normal(0, 0.1, n)
z += np.random.normal(0, 0.1, n)

# 2. Create the plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 3. Advanced Scatter parameters
# 'c' maps colors to the Z-axis
# 's' makes markers larger as they get further from the center
# 'alpha' prevents the plot from looking cluttered
# 'edgecolor' helps distinguish overlapping points
sizes = (x**2 + y**2) * 10
scatter = ax.scatter(x, y, z,
                     c=z,
                     cmap='magma',
                     s=sizes,
                     alpha=0.6,
                     edgecolors='w',
                     linewidth=0.5)

# 4. Customizing the view
ax.view_init(elev=20, azim=45) # Set the initial camera angle

# 5. Add a colorbar and labels
cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, pad=0.1)
cbar.set_label('Z-Value Intensity')

ax.set_title('Advanced 3D Scatter: Variable Size and Color Mapping')
ax.set_xlabel('X Dimension')
ax.set_ylabel('Y Dimension')
ax.set_zlabel('Z Dimension')

plt.show()