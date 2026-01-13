import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
def display_heightmap(height_map: np.ndarray):
  h, w = height_map.shape
  img = np.zeros((h, w, 3), dtype=np.uint8)

  # Mặc định: grayscale (đảo màu: 0 trắng, 255 đen)
  gray = 255 - height_map
  img[..., 0] = gray
  img[..., 1] = gray
  img[..., 2] = gray

  # Giá trị 100 -> RED
  mask = height_map == 100
  img[mask] = [255, 0, 0]

  plt.imshow(img)
  plt.title("Heightmap (100 = RED)")
  plt.axis("off")
  plt.show()

def red_heightmap(height_map: np.ndarray):
  heightmap = height_map.T
  # Custom colormap: white -> red
  cmap = LinearSegmentedColormap.from_list(
      "white_to_red",
      ["white", "red"]
  )

  # Chuẩn hóa 0–100
  norm = Normalize(vmin=50, vmax=100)
  #rotate heightmap for better visualization
  # heightmap = heightmap.T

  plt.imshow(np.rot90(heightmap, -1), cmap=cmap, norm=norm)
  plt.colorbar(label="Heightmap")
  plt.title("Heightmap")
  plt.axis("off")
  plt.show()

loaded_arr = np.load('./array_file.npy')
red_heightmap(loaded_arr)
print(loaded_arr)