import numpy as np
import matplotlib.pyplot as plt

# Tạo dữ liệu mô phỏng về hướng và tốc độ gió
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
U = -1 - X**2 + Y
V = 1 + X - Y**2

# Vẽ biểu đồ dòng chảy gió
plt.streamplot(X, Y, U, V, density=2)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Streamline Plot của dòng chảy gió')
plt.show()
