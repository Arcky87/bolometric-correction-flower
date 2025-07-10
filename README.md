# Bolometric Correction Utility

A Python command-line utility for calculating bolometric corrections for stars in the V band. This tool provides interpolated bolometric corrections based on stellar temperature, log(temperature), or B-V color index.

## Features

- **Multiple input methods**: Temperature (K), log(T), or B-V color index
- **Interpolation**: Cubic spline interpolation for smooth results between tabulated values
- **Interactive mode**: Console-based interactive queries
- **Batch processing**: Process multiple values from input files
- **Visualization**: Generate publication-quality plots
- **Comprehensive data**: Covers stellar temperatures from ~3,000K to ~57,000K

## Installation

### Prerequisites
- Python 3.7 or higher
- Required packages (install via pip):

```bash
pip install -r requirements.txt
```

### Clone the repository

```bash
git clone https://github.com/yourusername/bolometric-correction-utility.git
cd bolometric-correction-utility
```

## Usage

### Command Line Interface

#### Basic queries:

```bash
python bc_utility.py --temp 5780          # Sun's temperature (K)
python bc_utility.py --bv 0.65            # Red star B-V color
python bc_utility.py --logt 3.76          # Using log(temperature)
```

#### Interactive mode:

```bash
python bc_utility.py --interactive
```

#### Generate plots:

```bash
python bc_utility.py --plot               # Display plots
python bc_utility.py --plot --save-plots  # Save plots to files
```

#### Batch processing:

```bash
python bc_utility.py --batch input.txt
```

#### Get help:

```bash
python bc_utility.py --help
```

#### Interactive Mode Commands

```
BC> temp 5780     # Get BC from temperature
BC> bv 0.65       # Get BC from B-V color
BC> logt 3.76     # Get BC from log(temperature)
BC> info          # Show data ranges
BC> help          # Show commands
BC> quit          # Exit
```

### Batch File Format

#### Create a text file with one command per line:

```
# Comments start with #
temp 5780    # Sun
temp 10000   # Hot star
bv 0.0       # White star
bv 1.5       # Red star
logt 4.0     # Using log scale
```

## Data Range

* Temperature: 2,936 - 56,728 K
* log(T): 3.468 - 4.754
* B-V Color: -0.35 - 1.80
* Bolometric Correction: -5.535 - 0.035


## Examples

### Python Script Usage
```python
from bc_utility import load_bolometric_data, BolometricCorrection

# Load data and create utility
data = load_bolometric_data()
bc_util = BolometricCorrection(data)

# Single values
bc_sun = bc_util.get_BC_from_T(5780)  # Sun: BC ≈ -0.155
bc_red = bc_util.get_BC_from_BV(1.5)  # Red star

# Multiple values
temperatures = [4000, 5000, 6000, 7000]
bcs = bc_util.get_BC_from_T(temperatures)
```

### Command Line Examples

```bash
# Quick lookup
python bc_utility.py --temp 5780
# Output: T = 5780 K  →  BC = -0.155

# Multiple queries in interactive mode
python bc_utility.py -i
# BC> temp 10000
# T = 10000 K  →  BC = -0.488
# BC> bv 1.2
# B-V = 1.20  →  BC = -0.614
```

## Scientific Background

Bolometric corrections convert apparent magnitudes in specific photometric bands (V band in this case) to bolometric magnitudes, which represent the total energy output of a star across all wavelengths.

The relationship is: M_bol = M_V + BC_V

Where:
* M_bol = bolometric magnitude
* M_V = visual magnitude
* BC_V = bolometric correction for V band



## License

This project is licensed under the MIT License - see the LICENSE file for details.

### **LICENSE** (MIT License)
```txt
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

