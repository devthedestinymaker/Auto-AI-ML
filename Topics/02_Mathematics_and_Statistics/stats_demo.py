import numpy as np
import matplotlib.pyplot as plt
import os

# Use non-interactive backend for headless environments
plt.switch_backend('Agg')

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, 'normal_distribution.png')

# 1. Generate data following a Normal Distribution (Gaussian)
# Mean (mu) = 0, Standard Deviation (sigma) = 1
mu, sigma = 0, 1
data = np.random.normal(mu, sigma, 1000)

# 2. Visualize the distribution
plt.figure(figsize=(10, 6))
count, bins, ignored = plt.hist(data, 30, density=True, alpha=0.6, color='g', label='Histogram of Data')

# Plot the theoretical normal distribution curve
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
         np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
         linewidth=2, color='r', label='Theoretical Normal Curve')

plt.title('Normal Distribution Visualization')
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)

# Save the plot to the script's directory
plt.savefig(output_path)
print(f"Plot saved as '{output_path}'.")
# Don't call plt.show() in headless environment
