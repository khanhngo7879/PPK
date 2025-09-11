import pandas as pd
import matplotlib.pyplot as plt
from pyproj import Transformer
import re

# --- BƯỚC 1: LẤY REF POS TỪ .OBS (ECEF) ---
def get_ref_pos_from_obs(obs_file):
    with open(obs_file, 'r') as f:
        for line in f:
            if "APPROX POSITION XYZ" in line:
                match = re.match(r"\s*([-.\dEe+]+)\s+([-.\dEe+]+)\s+([-.\dEe+]+)", line)
                if match:
                    return tuple(map(float, match.groups()))
    raise ValueError("APPROX POSITION XYZ not found in obs file.")

# --- ECEF → geodetic ---
def ecef_to_geodetic(x, y, z):
    transformer = Transformer.from_crs("epsg:4978", "epsg:4326", always_xy=True)
    lon, lat, h = transformer.transform(x, y, z)
    return lat, lon, h

# --- BƯỚC 2: ĐỌC REF POS ---
obs_path = r"C:\rtk\Code\rtklib-py\data\u-blox\tmg23590.obs"
x, y, z = get_ref_pos_from_obs(obs_path)
ref_lat, ref_lon, ref_h = ecef_to_geodetic(x, y, z)
print(f"REF POS (lat, lon, h): {ref_lat}, {ref_lon}, {ref_h}")

# --- BƯỚC 3: ĐỌC FILE .POS ---
pos_path = r"C:\rtk\Code\rtklib-py\data\u-blox\rover.pos"
df = pd.read_csv(pos_path, delim_whitespace=True, comment='%', header=None)

# Đặt tên cột chính xác theo cấu trúc RTKLIB
df.columns = [
    "%","time", "latitude", "longitude", "height", "Q", "ns",
    "sdn", "sde", "sdu", "sdne", "sdeu", "sdun", "age", "ratio"
]

# Lọc ra các dòng dữ liệu hợp lệ
df = df[df["Q"].notna()]  # bỏ dòng trống nếu có

# --- BƯỚC 4: Chuyển sang ENU ---
transformer = Transformer.from_crs(
    "epsg:4326",
    f"+proj=tmerc +lat_0={ref_lat} +lon_0={ref_lon} +k=1 +x_0=0 +y_0=0 +ellps=WGS84",
    always_xy=True
)
east, north = transformer.transform(df["longitude"].values, df["latitude"].values)

# --- BƯỚC 5: VẼ ĐỒ THỊ ---
colors = {1: "green", 2: "orange", 5: "gray"}

plt.figure(figsize=(10, 6))
for q in df["Q"].unique():
    idx = df["Q"] == q
    plt.plot(east[idx], north[idx], '.', label=f"Q={q}", color=colors.get(q, 'black'))

plt.xlabel("East (m)")
plt.ylabel("North (m)")
plt.title("PPK Trajectory with Quality Coloring")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

