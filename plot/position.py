import pandas as pd
import matplotlib.pyplot as plt
from pyproj import Transformer
import re

# 📌 1. Đọc ref pos (ECEF) từ file .obs
def get_ref_pos_from_obs(obs_file):
    with open(obs_file, 'r') as f:
        for line in f:
            if "APPROX POSITION XYZ" in line:
                match = re.match(r"\s*([-.\dEe+]+)\s+([-.\dEe+]+)\s+([-.\dEe+]+)", line)
                if match:
                    x, y, z = map(float, match.groups())
                    return x, y, z
    raise ValueError("APPROX POSITION XYZ not found")

# 🔁 ECEF → WGS84
def ecef_to_geodetic(x, y, z):
    transformer = Transformer.from_crs("epsg:4978", "epsg:4326", always_xy=True)
    lon, lat, h = transformer.transform(x, y, z)
    return lat, lon, h

# 📍2. Đọc tọa độ tham chiếu
obs_path = r"C:\rtk\Code\rtklib-py\data\u-blox\tmg23590.obs"
ecef = get_ref_pos_from_obs(obs_path)
ref_lat, ref_lon, ref_h = ecef_to_geodetic(*ecef)
print(f"REF POS (lat, lon, h): {ref_lat}, {ref_lon}, {ref_h}")

# 📈 3. Đọc dữ liệu .pos
pos_path = r"C:\rtk\Code\rtklib-py\data\u-blox\rover.pos"
df = pd.read_csv(pos_path, delim_whitespace=True, comment='%', header=None)

# Đặt tên cột (tùy file)
df.columns = [
    "%","time", "latitude", "longitude", "height", "Q", "ns",
    "sdn", "sde", "sdu", "sdne", "sdeu", "sdun", "age", "ratio"
]

# 🔁 4. Chuyển sang ENU
transformer = Transformer.from_crs(
    "epsg:4326",
    f"+proj=tmerc +lat_0={ref_lat} +lon_0={ref_lon} +k=1 +x_0=0 +y_0=0 +ellps=WGS84",
    always_xy=True
)
east, north = transformer.transform(df["longitude"].values, df["latitude"].values)
up = df["height"].values - ref_h

# 👉 Thêm cột thời gian (epoch)
df["t"] = range(len(df))

# 🖼️ 5. Vẽ biểu đồ Position
plt.figure(figsize=(10, 6))
plt.plot(df["t"], east, label="East")
plt.plot(df["t"], north, label="North")
plt.plot(df["t"], up, label="Up")
plt.legend()
plt.title("Position over time")
plt.xlabel("Epoch")
plt.ylabel("Meters")
plt.grid(True)
plt.tight_layout()
plt.show()
