import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Transformer
import re

# 📌 Đọc ref pos từ file base.obs
def get_ref_pos_from_obs(obs_file):
    with open(obs_file, 'r') as f:
        for line in f:
            match = re.match(r"\s*([-.\dEe+]+)\s+([-.\dEe+]+)\s+([-.\dEe+]+)\s+APPROX POSITION XYZ", line)
            if match:
                x, y, z = map(float, match.groups())
                return x, y, z
    raise ValueError("APPROX POSITION XYZ not found")

# 🔁 ECEF → geodetic (lat, lon, h)
def ecef_to_geodetic(x, y, z):
    transformer = Transformer.from_crs("epsg:4978", "epsg:4326", always_xy=True)
    lon, lat, h = transformer.transform(x, y, z)
    return lat, lon, h

# 📍 Đọc ref toạ độ từ base.obs
obs_path = r"C:\\rtk\\Code\\rtklib-py\\data\\u-blox\\tmg23590.obs"
ecef = get_ref_pos_from_obs(obs_path)
ref_lat, ref_lon, ref_h = ecef_to_geodetic(*ecef)

# 📍 Đọc dữ liệu .pos
df = pd.read_csv("data/u-blox/rover.pos", delim_whitespace=True, comment='%')
df.columns = [
    "%","time", "latitude", "longitude", "height", "Q", "ns",
    "sdn", "sde", "sdu", "sdne", "sdeu", "sdun", "age", "ratio"
]

# Chuyển vị trí sang ENU
transformer = Transformer.from_crs(
    "epsg:4326",
    f"+proj=tmerc +lat_0={ref_lat} +lon_0={ref_lon} +k=1 +x_0=0 +y_0=0 +ellps=WGS84",
    always_xy=True
)
east, north = transformer.transform(df["longitude"].values, df["latitude"].values)
up = df["height"].values - ref_h

# Tính vận tốc (m/epoch) bằng đạo hàm
ve = np.gradient(east)
vn = np.gradient(north)
vu = np.gradient(up)
v_total = np.sqrt(ve**2 + vn**2 + vu**2)

# Gắn trục thời gian
df["t"] = range(len(df))

# Vẽ đồ thị vận tốc
plt.figure(figsize=(10, 6))
plt.plot(df["t"], ve, label="V_East")
plt.plot(df["t"], vn, label="V_North")
plt.plot(df["t"], vu, label="V_Up")
plt.plot(df["t"], v_total, label="V_Total", linestyle='--', color='black')
plt.title("Velocity over time")
plt.xlabel("Epoch")
plt.ylabel("Velocity (m/epoch)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
