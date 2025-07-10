#!/usr/bin/env python3
"""
Bolometric Correction Utility - Console Application
Calculate bolometric corrections for stars in V band

Usage:
    python bc_utility.py --help
    python bc_utility.py --temp 5780
    python bc_utility.py --bv 0.65
    python bc_utility.py --interactive
    python bc_utility.py --plot --save-plots
    python bc_utility.py --batch input.txt
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd
from io import StringIO
import argparse
import sys
import os

class BolometricCorrection:
    def __init__(self, data):
        """Initialize the bolometric correction utility"""
        self.data = data.copy()
        self.data = self.data.sort_values('T')
        
        # Create interpolation functions
        self.bc_from_T = interp1d(self.data['T'], self.data['BC'], 
                                  kind='cubic', bounds_error=False, 
                                  fill_value='extrapolate')
        self.bc_from_logT = interp1d(self.data['logT'], self.data['BC'], 
                                     kind='cubic', bounds_error=False, 
                                     fill_value='extrapolate')
        self.bc_from_BV = interp1d(self.data['B_V'], self.data['BC'], 
                                   kind='cubic', bounds_error=False, 
                                   fill_value='extrapolate')
        
        # Temperature range
        self.T_min, self.T_max = self.data['T'].min(), self.data['T'].max()
        self.logT_min, self.logT_max = self.data['logT'].min(), self.data['logT'].max()
        self.BV_min, self.BV_max = self.data['B_V'].min(), self.data['B_V'].max()
    
    def get_BC_from_T(self, temperature, verbose=True):
        """Get bolometric correction for given temperature(s)"""
        T = np.asarray(temperature)
        
        if verbose and (np.any(T < self.T_min) or np.any(T > self.T_max)):
            print(f"Warning: Temperature outside range [{self.T_min:.0f}, {self.T_max:.0f}] K")
            print("Extrapolation will be used.")
        
        return self.bc_from_T(T)
    
    def get_BC_from_logT(self, log_temperature, verbose=True):
        """Get bolometric correction for given log(T)"""
        logT = np.asarray(log_temperature)
        
        if verbose and (np.any(logT < self.logT_min) or np.any(logT > self.logT_max)):
            print(f"Warning: log(T) outside range [{self.logT_min:.3f}, {self.logT_max:.3f}]")
            print("Extrapolation will be used.")
        
        return self.bc_from_logT(logT)
    
    def get_BC_from_BV(self, b_v_color, verbose=True):
        """Get bolometric correction for given B-V color"""
        BV = np.asarray(b_v_color)
        
        if verbose and (np.any(BV < self.BV_min) or np.any(BV > self.BV_max)):
            print(f"Warning: B-V outside range [{self.BV_min:.2f}, {self.BV_max:.2f}]")
            print("Extrapolation will be used.")
        
        return self.bc_from_BV(BV)

def load_bolometric_data():
    """Load the bolometric correction data"""
    data = """
-0.35 4.7538 -4.720 56728
-0.34 4.7031 -4.506 50477
-0.33 4.6551 -4.197 45196
-0.32 4.6098 -3.861 40719
-0.31 4.5670 -3.534 36897
-0.30 4.5266 -3.234 33620
-0.29 4.4884 -2.966 30789
-0.28 4.4523 -2.730 28333
-0.27 4.4183 -2.523 26199
-0.26 4.3863 -2.341 24338
-0.25 4.3561 -2.177 22703
-0.24 4.3276 -2.028 21261
-0.23 4.3008 -1.891 19989
-0.22 4.2755 -1.762 18858
-0.21 4.2517 -1.641 17852
-0.20 4.2294 -1.525 16958
-0.19 4.2083 -1.414 16154
-0.18 4.1885 -1.307 15434
-0.17 4.1699 -1.205 14787
-0.16 4.1524 -1.107 14203
-0.15 4.1360 -1.013 13677
-0.14 4.1205 -0.923 13197
-0.13 4.1060 -0.839 12764
-0.12 4.0923 -0.759 12368
-0.11 4.0795 -0.684 12008
-0.10 4.0674 -0.614 11678
-0.09 4.0560 -0.549 11376
-0.08 4.0453 -0.488 11099
-0.07 4.0353 -0.432 10846
-0.06 4.0258 -0.381 10612
-0.05 4.0169 -0.334 10396
-0.04 4.0084 -0.290 10195
-0.03 4.0005 -0.252 10011
-0.02 3.9930 -0.216 9840
-0.01 3.9859 -0.184 9680
0.00 3.9791 -0.155 9530
0.01 3.9728 -0.129 9392
0.02 3.9667 -0.106 9261
0.03 3.9609 -0.085 9139
0.04 3.9555 -0.067 9026
0.05 3.9502 -0.050 8916
0.06 3.9452 -0.036 8814
0.07 3.9404 -0.024 8717
0.08 3.9358 -0.013 8625
0.09 3.9314 -0.004 8538
0.10 3.9271 0.004 8454
0.11 3.9229 0.010 8373
0.12 3.9189 0.015 8296
0.13 3.9150 0.019 8222
0.14 3.9113 0.022 8152
0.15 3.9076 0.024 8083
0.16 3.9040 0.026 8016
0.17 3.9004 0.028 7950
0.18 3.8969 0.029 7886
0.19 3.8935 0.031 7825
0.20 3.8902 0.032 7766
0.21 3.8869 0.033 7707
0.22 3.8836 0.033 7648
0.23 3.8804 0.034 7592
0.24 3.8771 0.034 7535
0.25 3.8740 0.035 7481
0.26 3.8708 0.035 7426
0.27 3.8676 0.035 7372
0.28 3.8645 0.035 7319
0.29 3.8614 0.035 7267
0.30 3.8583 0.034 7216
0.31 3.8552 0.034 7164
0.32 3.8521 0.033 7113
0.33 3.8490 0.032 7063
0.34 3.8460 0.031 7014
0.35 3.8429 0.030 6964
0.36 3.8399 0.028 6916
0.37 3.8368 0.026 6867
0.38 3.8338 0.025 6820
0.39 3.8307 0.022 6771
0.40 3.8277 0.020 6725
0.41 3.8247 0.018 6678
0.42 3.8217 0.015 6632
0.43 3.8187 0.012 6587
0.44 3.8157 0.009 6541
0.45 3.8127 0.006 6496
0.46 3.8098 0.003 6453
0.47 3.8068 -0.001 6409
0.48 3.8039 -0.004 6366
0.49 3.8010 -0.008 6324
0.50 3.7981 -0.012 6282
0.51 3.7952 -0.016 6240
0.52 3.7923 -0.021 6198
0.53 3.7895 -0.025 6158
0.54 3.7866 -0.030 6117
0.55 3.7838 -0.035 6078
0.56 3.7811 -0.039 6040
0.57 3.7783 -0.045 6002
0.58 3.7756 -0.050 5964
0.59 3.7729 -0.055 5927
0.60 3.7702 -0.061 5891
0.61 3.7676 -0.067 5855
0.62 3.7649 -0.073 5819
0.63 3.7623 -0.079 5784
0.64 3.7598 -0.085 5751
0.65 3.7572 -0.091 5717
0.66 3.7547 -0.098 5684
0.67 3.7523 -0.104 5653
0.68 3.7498 -0.111 5620
0.69 3.7474 -0.117 5589
0.70 3.7450 -0.124 5559
0.71 3.7426 -0.132 5528
0.72 3.7403 -0.139 5499
0.73 3.7380 -0.146 5470
0.74 3.7358 -0.153 5442
0.75 3.7335 -0.161 5413
0.76 3.7313 -0.168 5386
0.77 3.7291 -0.176 5359
0.78 3.7270 -0.184 5333
0.79 3.7249 -0.192 5307
0.80 3.7228 -0.200 5282
0.81 3.7207 -0.208 5256
0.82 3.7186 -0.216 5231
0.83 3.7166 -0.225 5207
0.84 3.7146 -0.233 5183
0.85 3.7126 -0.242 5159
0.86 3.7107 -0.250 5136
0.87 3.7088 -0.259 5114
0.88 3.7068 -0.268 5090
0.89 3.7049 -0.277 5068
0.90 3.7031 -0.285 5047
0.91 3.7012 -0.295 5025
0.92 3.6994 -0.304 5004
0.93 3.6976 -0.313 4984
0.94 3.6958 -0.322 4963
0.95 3.6940 -0.332 4943
0.96 3.6922 -0.342 4922
0.97 3.6904 -0.352 4902
0.98 3.6887 -0.361 4883
0.99 3.6869 -0.372 4862
1.00 3.6852 -0.382 4843
1.01 3.6835 -0.392 4825
1.02 3.6818 -0.403 4806
1.03 3.6800 -0.414 4786
1.04 3.6783 -0.426 4767
1.05 3.6766 -0.437 4748
1.06 3.6750 -0.448 4731
1.07 3.6733 -0.459 4713
1.08 3.6716 -0.471 4694
1.09 3.6699 -0.482 4676
1.10 3.6682 -0.494 4658
1.11 3.6666 -0.505 4640
1.12 3.6649 -0.517 4622
1.13 3.6633 -0.528 4605
1.14 3.6616 -0.540 4587
1.15 3.6599 -0.552 4569
1.16 3.6583 -0.564 4553
1.17 3.6566 -0.576 4535
1.18 3.6550 -0.588 4518
1.19 3.6533 -0.601 4500
1.20 3.6516 -0.614 4483
1.21 3.6500 -0.626 4466
1.22 3.6483 -0.640 4449
1.23 3.6467 -0.652 4433
1.24 3.6450 -0.666 4415
1.25 3.6434 -0.679 4399
1.26 3.6417 -0.694 4382
1.27 3.6401 -0.707 4366
1.28 3.6384 -0.722 4349
1.29 3.6368 -0.736 4333
1.30 3.6351 -0.752 4316
1.31 3.6335 -0.766 4300
1.32 3.6318 -0.782 4283
1.33 3.6301 -0.798 4266
1.34 3.6285 -0.814 4251
1.35 3.6268 -0.831 4234
1.36 3.6251 -0.848 4217
1.37 3.6235 -0.865 4202
1.38 3.6218 -0.883 4186
1.39 3.6201 -0.901 4169
1.40 3.6184 -0.920 4153
1.41 3.6167 -0.939 4137
1.42 3.6149 -0.960 4120
1.43 3.6132 -0.980 4103
1.44 3.6114 -1.002 4086
1.45 3.6096 -1.024 4070
1.46 3.6078 -1.047 4053
1.47 3.6060 -1.071 4036
1.48 3.6041 -1.096 4018
1.49 3.6022 -1.122 4001
1.50 3.6002 -1.150 3982
1.51 3.5982 -1.178 3964
1.52 3.5961 -1.209 3945
1.53 3.5940 -1.241 3926
1.54 3.5918 -1.276 3906
1.55 3.5895 -1.312 3885
1.56 3.5872 -1.350 3865
1.57 3.5847 -1.393 3843
1.58 3.5822 -1.437 3821
1.59 3.5795 -1.486 3797
1.60 3.5767 -1.539 3773
1.61 3.5738 -1.595 3748
1.62 3.5707 -1.658 3721
1.63 3.5674 -1.728 3693
1.64 3.5640 -1.802 3664
1.65 3.5604 -1.885 3634
1.66 3.5565 -1.978 3601
1.67 3.5525 -2.078 3568
1.68 3.5482 -2.191 3533
1.69 3.5436 -2.318 3496
1.70 3.5387 -2.460 3457
1.71 3.5335 -2.620 3415
1.72 3.5279 -2.803 3372
1.73 3.5220 -3.007 3326
1.74 3.5157 -3.239 3278
1.75 3.5090 -3.502 3228
1.76 3.5018 -3.805 3175
1.77 3.4941 -4.152 3119
1.78 3.4860 -4.544 3061
1.79 3.4772 -5.004 3000
1.80 3.4678 -5.535 2936
"""
    
    df = pd.read_csv(StringIO(data.strip()), sep=r'\s+', 
                     names=['B_V', 'logT', 'BC', 'T'])
    return df

def save_plots(data, output_dir="plots"):
    """Save plots to files instead of displaying them"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Set matplotlib to non-interactive backend
    plt.ioff()
    
    # Main plots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Bolometric Corrections for V Band', fontsize=16, fontweight='bold')
    
    # Plot 1: BC vs Temperature
    axes[0,0].plot(data['T'], data['BC'], 'b.-', linewidth=2, markersize=4)
    axes[0,0].set_xlabel('Temperature (K)')
    axes[0,0].set_ylabel('Bolometric Correction (BC)')
    axes[0,0].set_title('BC vs Temperature')
    axes[0,0].grid(True, alpha=0.3)
    axes[0,0].invert_xaxis()
    
    # Plot 2: BC vs log(T)
    axes[0,1].plot(data['logT'], data['BC'], 'r.-', linewidth=2, markersize=4)
    axes[0,1].set_xlabel('log(T)')
    axes[0,1].set_ylabel('Bolometric Correction (BC)')
    axes[0,1].set_title('BC vs log(Temperature)')
    axes[0,1].grid(True, alpha=0.3)
    axes[0,1].invert_xaxis()
    
    # Plot 3: BC vs B-V color
    axes[1,0].plot(data['B_V'], data['BC'], 'g.-', linewidth=2, markersize=4)
    axes[1,0].set_xlabel('B-V Color Index')
    axes[1,0].set_ylabel('Bolometric Correction (BC)')
    axes[1,0].set_title('BC vs B-V Color')
    axes[1,0].grid(True, alpha=0.3)
    
    # Plot 4: Temperature vs B-V
    axes[1,1].plot(data['B_V'], data['T'], 'm.-', linewidth=2, markersize=4)
    axes[1,1].set_xlabel('B-V Color Index')
    axes[1,1].set_ylabel('Temperature (K)')
    axes[1,1].set_title('Temperature vs B-V Color')
    axes[1,1].grid(True, alpha=0.3)
    axes[1,1].set_yscale('log')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bolometric_corrections.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    scatter = ax.scatter(data['B_V'], data['T'], data['BC'], 
                        c=data['BC'], cmap='viridis', s=30)
    ax.set_xlabel('B-V Color Index')
    ax.set_ylabel('Temperature (K)')
    ax.set_zlabel('Bolometric Correction')
    ax.set_title('3D View: BC vs B-V vs Temperature')
    
    plt.colorbar(scatter, label='Bolometric Correction')
    plt.savefig(os.path.join(output_dir, 'bolometric_corrections_3d.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Plots saved to {output_dir}/ directory")

def interactive_mode(bc_util):
    """Interactive console mode"""
    print("\n" + "="*60)
    print("BOLOMETRIC CORRECTION UTILITY - Interactive Mode")
    print("="*60)
    print("\nCommands:")
    print("  temp <value>     - Get BC from temperature (K)")
    print("  logt <value>     - Get BC from log(temperature)")
    print("  bv <value>       - Get BC from B-V color")
    print("  info             - Show data range information")
    print("  help             - Show this help")
    print("  quit             - Exit")
    print("-"*60)
    
    while True:
        try:
            cmd = input("\nBC> ").strip().lower()
            
            if cmd in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            elif cmd == 'help':
                print("\nCommands:")
                print("  temp <value>     - Get BC from temperature (K)")
                print("  logt <value>     - Get BC from log(temperature)")
                print("  bv <value>       - Get BC from B-V color")
                print("  info             - Show data range information")
                print("  help             - Show this help")
                print("  quit             - Exit")
            elif cmd == 'info':
                print(f"\nData ranges:")
                print(f"  Temperature: {bc_util.T_min:.0f} - {bc_util.T_max:.0f} K")
                print(f"  log(T):      {bc_util.logT_min:.3f} - {bc_util.logT_max:.3f}")
                print(f"  B-V:         {bc_util.BV_min:.2f} - {bc_util.BV_max:.2f}")
                print(f"  BC:          {bc_util.data['BC'].min():.3f} - {bc_util.data['BC'].max():.3f}")
                print(f"  Data points: {len(bc_util.data)}")
            elif cmd.startswith('temp '):
                try:
                    value = float(cmd.split()[1])
                    bc = bc_util.get_BC_from_T(value)
                    print(f"T = {value:.0f} K  →  BC = {bc:.3f}")
                except (ValueError, IndexError):
                    print("Error: Please provide a valid temperature value")
            elif cmd.startswith('logt '):
                try:
                    value = float(cmd.split()[1])
                    bc = bc_util.get_BC_from_logT(value)
                    print(f"log(T) = {value:.3f}  →  BC = {bc:.3f}")
                except (ValueError, IndexError):
                    print("Error: Please provide a valid log(T) value")
            elif cmd.startswith('bv '):
                try:
                    value = float(cmd.split()[1])
                    bc = bc_util.get_BC_from_BV(value)
                    print(f"B-V = {value:.2f}  →  BC = {bc:.3f}")
                except (ValueError, IndexError):
                    print("Error: Please provide a valid B-V value")
            elif cmd == '':
                continue
            else:
                print(f"Unknown command: {cmd}")
                print("Type 'help' for available commands")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break

def batch_process(filename, bc_util):
    """Process batch input from file"""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        print(f"\nProcessing batch file: {filename}")
        print("-" * 50)
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            parts = line.split()
            if len(parts) < 2:
                print(f"Line {i}: Invalid format - {line}")
                continue
                
            cmd = parts[0].lower()
            try:
                value = float(parts[1])
                
                if cmd in ['temp', 't', 'temperature']:
                    bc = bc_util.get_BC_from_T(value, verbose=False)
                    print(f"T = {value:.0f} K  →  BC = {bc:.3f}")
                elif cmd in ['logt', 'log', 'logtemp']:
                    bc = bc_util.get_BC_from_logT(value, verbose=False)
                    print(f"log(T) = {value:.3f}  →  BC = {bc:.3f}")
                elif cmd in ['bv', 'color', 'b-v']:
                    bc = bc_util.get_BC_from_BV(value, verbose=False)
                    print(f"B-V = {value:.2f}  →  BC = {bc:.3f}")
                else:
                    print(f"Line {i}: Unknown command '{cmd}' - {line}")
                    
            except ValueError:
                print(f"Line {i}: Invalid value '{parts[1]}' - {line}")
                
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Bolometric Correction Utility for V Band',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --temp 5780                    # Sun's temperature
  %(prog)s --bv 0.65                      # Red star color
  %(prog)s --logt 3.76                    # Using log(T)
  %(prog)s --interactive                  # Interactive mode
  %(prog)s --plot --save-plots             # Generate and save plots
  %(prog)s --batch input.txt              # Process batch file
  %(prog)s --info                         # Show data information

Batch file format (one per line):
  temp 5780
  bv 0.65
  logt 3.76
  # Comments start with #
        """)
    
    parser.add_argument('--temp', '-t', type=float, 
                       help='Temperature in Kelvin')
    parser.add_argument('--logt', type=float,
                       help='log(Temperature)')
    parser.add_argument('--bv', type=float,
                       help='B-V color index')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Start interactive mode')
    parser.add_argument('--plot', '-p', action='store_true',
                       help='Generate plots')
    parser.add_argument('--save-plots', action='store_true',
                       help='Save plots to files instead of displaying')
    parser.add_argument('--batch', '-b', metavar='FILE',
                       help='Process batch input file')
    parser.add_argument('--info', action='store_true',
                       help='Show data information')
    parser.add_argument('--output', '-o', default='results.txt',
                       help='Output file for batch results')
    
    args = parser.parse_args()
    
    # Load data and create utility
    print("Loading bolometric correction data...")
    data = load_bolometric_data()
    bc_util = BolometricCorrection(data)
    print("Data loaded successfully.")
    
    # Handle different modes
    if args.info:
        print(f"\nBolometric Correction Data Information:")
        print(f"Temperature range: {bc_util.T_min:.0f} - {bc_util.T_max:.0f} K")
        print(f"log(T) range:      {bc_util.logT_min:.3f} - {bc_util.logT_max:.3f}")
        print(f"B-V range:         {bc_util.BV_min:.2f} - {bc_util.BV_max:.2f}")
        print(f"BC range:          {data['BC'].min():.3f} - {data['BC'].max():.3f}")
        print(f"Number of points:  {len(data)}")
        
    if args.plot:
        if args.save_plots:
            save_plots(data)
        else:
            # Import here to avoid issues when saving plots
            from matplotlib import pyplot as plt
            
            # Create plots (original plotting function)
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Bolometric Corrections for V Band', fontsize=16, fontweight='bold')
            
            axes[0,0].plot(data['T'], data['BC'], 'b.-', linewidth=2, markersize=4)
            axes[0,0].set_xlabel('Temperature (K)')
            axes[0,0].set_ylabel('Bolometric Correction (BC)')
            axes[0,0].set_title('BC vs Temperature')
            axes[0,0].grid(True, alpha=0.3)
            axes[0,0].invert_xaxis()
            
            axes[0,1].plot(data['logT'], data['BC'], 'r.-', linewidth=2, markersize=4)
            axes[0,1].set_xlabel('log(T)')
            axes[0,1].set_ylabel('Bolometric Correction (BC)')
            axes[0,1].set_title('BC vs log(Temperature)')
            axes[0,1].grid(True, alpha=0.3)
            axes[0,1].invert_xaxis()
            
            axes[1,0].plot(data['B_V'], data['BC'], 'g.-', linewidth=2, markersize=4)
            axes[1,0].set_xlabel('B-V Color Index')
            axes[1,0].set_ylabel('Bolometric Correction (BC)')
            axes[1,0].set_title('BC vs B-V Color')
            axes[1,0].grid(True, alpha=0.3)
            
            axes[1,1].plot(data['B_V'], data['T'], 'm.-', linewidth=2, markersize=4)
            axes[1,1].set_xlabel('B-V Color Index')
            axes[1,1].set_ylabel('Temperature (K)')
            axes[1,1].set_title('Temperature vs B-V Color')
            axes[1,1].grid(True, alpha=0.3)
            axes[1,1].set_yscale('log')
            
            plt.tight_layout()
            plt.show()
            
    if args.temp is not None:
        bc = bc_util.get_BC_from_T(args.temp)
        print(f"T = {args.temp:.0f} K  →  BC = {bc:.3f}")
        
    if args.logt is not None:
        bc = bc_util.get_BC_from_logT(args.logt)
        print(f"log(T) = {args.logt:.3f}  →  BC = {bc:.3f}")
        
    if args.bv is not None:
        bc = bc_util.get_BC_from_BV(args.bv)
        print(f"B-V = {args.bv:.2f}  →  BC = {bc:.3f}")
        
    if args.batch:
        batch_process(args.batch, bc_util)
        
    if args.interactive:
        interactive_mode(bc_util)
        
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()

if __name__ == "__main__":
    main()

