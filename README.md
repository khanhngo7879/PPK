# RTKLIB-Python: Post-Processing Kinematic (PPK) GNSS Solution

A Python implementation of Real-Time Kinematic (RTK) and Post-Processing Kinematic (PPK) GNSS positioning algorithms, inspired by RTKLIB. This project provides high-precision positioning capabilities using dual-frequency GNSS observations from rover and base stations.

## 🚀 Features

- **Dual-frequency GNSS processing** (GPS, GLONASS, Galileo)
- **Multiple processing modes**: Forward, Backward, Combined solutions
- **Integer ambiguity resolution** using Modified LAMBDA algorithm
- **Cycle slip detection** using Doppler and geometry-free combinations  
- **Comprehensive quality control** with outlier detection
- **Multiple receiver support**: u-blox F9P, smartphone GNSS, and others
- **Visualization tools** for trajectory analysis and quality assessment

## 📁 Project Structure

```
src/
├── __ppk_config.py         # Main configuration file
├── config_f9p.py           # Configuration for u-blox F9P receivers  
├── config_phone.py         # Configuration for smartphone GNSS
├── run_ppk.py              # Main execution script
├── rtkpos.py               # Core PPK positioning algorithms
├── rtkcmn.py               # Common GNSS functions and utilities
├── rinex.py                # RINEX file reader and parser
├── ephemeris.py            # Satellite orbit and clock computations
├── pntpos.py               # Single-point positioning (SPP)
├── mlambda.py              # Modified LAMBDA ambiguity resolution
└── postpos.py              # Post-processing workflow management

plot/
├── accel.py                # Acceleration analysis and plotting
├── gndTrk.py               # Ground track visualization  
├── numberSat.py            # Satellite count over time
├── position.py             # Position time series plots
└── velocity.py             # Velocity analysis and plotting

data/
└── u-blox/                 # Sample data directory
    ├── rover.obs           # Rover observation file (RINEX)
    ├── rover.nav           # Navigation/ephemeris file
    └── tmg23590.obs        # Base station observations
```

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- Required packages:

```bash
pip install numpy pandas matplotlib pyproj
```

### Setup
1. Clone the repository:
```bash
git clone https://your-gitlab-url/ppk-project.git
cd ppk-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📋 Usage

### Basic PPK Processing

1. **Prepare your data**: Place RINEX observation files (.obs) and navigation files (.nav) in the data directory.

2. **Configure processing parameters**: Edit the appropriate config file:
   - `config_f9p.py` for u-blox F9P receivers
   - `config_phone.py` for smartphone GNSS
   - `__ppk_config.py` for custom configurations

3. **Run PPK processing**:
```bash
cd src
python run_ppk.py
```

4. **View results**: The solution will be saved as `.pos` files with statistics in `.pos.stat` files.

### Configuration Options

Key parameters you can adjust:

```python
# Processing mode
pmode = 'kinematic'          # 'static' or 'kinematic'
filtertype = 'forward'       # 'forward', 'backward', 'combined'

# Quality control
elmin = 15                   # Minimum elevation angle (degrees)
cnr_min = [35, 35]          # Minimum signal strength (dB-Hz)

# Ambiguity resolution
armode = 3                   # 0:off, 1:continuous, 3:fix-and-hold
thresar = 3                  # AR validation threshold
```

### Example Usage

```python
# Basic processing workflow
import __ppk_config as cfg
from rtkpos import rtkinit
from postpos import procpos

# Initialize
nav = rtkinit(cfg)

# Load observations
rov = rnx_decode(cfg)
rov.decode_obsfile(nav, 'rover.obs', None)

base = rnx_decode(cfg) 
base.decode_obsfile(nav, 'base.obs', None)

# Process solution
sol = procpos(nav, rov, base, fp_stat)
```

## 📊 Visualization and Analysis

The project includes several plotting utilities:

```bash
cd plot
python position.py      # Position time series
python velocity.py      # Velocity analysis  
python accel.py         # Acceleration plots
python gndTrk.py        # Ground track with quality coloring
python numberSat.py     # Satellite availability
```

### Output Formats

**Position file (.pos)**:
```
%  GPST          latitude(deg) longitude(deg)  height(m)   Q  ns   sdn(m)   sde(m)   sdu(m)
2158  259200.000   37.123456789 -122.987654321    123.456   1  12   0.0123   0.0089   0.0156
```

Quality indicators (Q):
- 1: Fixed solution
- 2: Float solution  
- 4: DGPS solution
- 5: Single-point solution

## ⚙️ Algorithm Details

### Core Features

- **Kalman Filter**: Extended Kalman filter for state estimation with position, velocity, acceleration, and carrier phase ambiguity states
- **Double Differencing**: Eliminates receiver clock errors and reduces atmospheric effects
- **Cycle Slip Detection**: Multiple methods including Doppler consistency and geometry-free combinations
- **Ambiguity Resolution**: Modified LAMBDA method with partial fixing and validation
- **Quality Control**: Comprehensive outlier detection and satellite exclusion

### Supported Systems
- GPS (L1/L2)
- GLONASS (G1/G2)  
- Galileo (E1/E5b)
- Multi-constellation processing

## 📈 Performance

Typical accuracy (with proper base-rover setup):
- **Horizontal**: 1-5 cm (fixed solution)
- **Vertical**: 2-8 cm (fixed solution)  
- **Baseline range**: Up to 20-30 km

## 🔧 Troubleshooting

### Common Issues

**Low fix rate:**
- Check base-rover distance (keep < 20 km)
- Verify data quality and satellite availability
- Adjust AR threshold (`thresar`)

**No solution:**
- Verify file formats (RINEX 3.x)
- Check observation overlap between base/rover
- Ensure proper base station coordinates

**Poor accuracy:**
- Check for multipath environment
- Verify antenna setup and orientation
- Review elevation mask settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)  
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original RTKLIB by T. Takasu
- CSSRLIB by Rui Hirokawa  
- Modified LAMBDA method by X.-W. Chang et al.

## 📞 Support

For questions and support:
- Create an issue on GitLab
- Check the troubleshooting section
- Review configuration examples

## 🔗 Related Projects

- [RTKLIB](http://www.rtklib.com/) - Original C implementation
- [CSSRLIB](https://github.com/hirokawa/cssrlib) - State-space approach GNSS library

---

**Keywords**: GNSS, RTK, PPK, GPS, positioning, surveying, navigation, python, RINEX