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

# Tính gia tốc (m/epoch²) bằng đạo hàm bậc hai
ae = np.gradient(np.gradient(east))
an = np.gradient(np.gradient(north))
au = np.gradient(np.gradient(up))
a_total = np.sqrt(ae**2 + an**2 + au**2)

# Gắn trục thời gian
df["t"] = range(len(df))

# Vẽ đồ thị gia tốc
plt.figure(figsize=(10, 6))
plt.plot(df["t"], ae, label="A_East")
plt.plot(df["t"], an, label="A_North")
plt.plot(df["t"], au, label="A_Up")
plt.plot(df["t"], a_total, label="A_Total", linestyle='--', color='black')
plt.title("Acceleration over time")
plt.xlabel("Epoch")
plt.ylabel("Acceleration (m/epoch²)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
