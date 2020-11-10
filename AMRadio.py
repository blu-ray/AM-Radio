from Radio.Radio import Radio, Signal
import os
import sys
import subprocess
import argparse
from scipy.io import wavfile as wav

parser = argparse.ArgumentParser()
# Setting the arguments of the command line interface
parser.add_argument("-v", type=str, required=True, help="Path to the Data file")
parser.add_argument("-f", type=int, required=True, help="Carrier Frequency in KHz")
parser.add_argument("-e", type=float, required=True, help="Peak approximation error")
parser.add_argument("-o", type=str, required=True, help="Path to the output wav file")
parser.add_argument('-p', required=False, help="Play the sound", action='store_true')

args = parser.parse_args()  # Getting and parsing the arguments
signal: Signal = Signal.generate_from_file(args.v, 480)     # Reading signal from the input file
radio: Radio = Radio(signal, args.e)    # Creating the radio instance
desired_sig: Signal = radio.demodulate(args.f)  # Demodulating the desired signal
wav.write(args.o, desired_sig.sampling_rate, desired_sig.value.astype("int16"))    # Writing the result to the output file
if args.p:  # Playing the sound if the `p` argument has been set.
    if sys.platform == "win32":     # Playing the sound in the windows
        os.system(f"explorer {args.o}")
    elif sys.platform == 'Darwin':       # macOS
        subprocess.call(('open', args.o))
    else:   # Playing the sound in the linux.
        subprocess.run(['xdg-open', args.o], check=True)
