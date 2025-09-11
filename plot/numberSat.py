import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/u-blox/rover.pos", delim_whitespace=True, comment='%')
df.columns = [
    "%","time", "latitude", "longitude", "height", "Q", "ns",
    "sdn", "sde", "sdu", "sdne", "sdeu", "sdun", "age", "ratio"
]

df["t"] = range(len(df))

plt.figure(figsize=(10, 4))
plt.plot(df["t"], df["ns"], label="Number of Satellites")
plt.xlabel("Epoch")
plt.ylabel("Nsat")
plt.title("Number of Satellites over Time")
plt.grid(True)
plt.tight_layout()
plt.show()
