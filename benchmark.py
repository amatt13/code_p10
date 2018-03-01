import subprocess
import argparse
import os
import sys
import datetime

my_location = os.path.dirname(os.path.realpath(__file__)) + '/'
linux = 'linux'

def linux_machine(OS_name: str):
    return OS_name == linux

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Benchmark tool for UPPAAL models')
    parser.add_argument('-o',  type=str, required=False, help='OS name')
    parser.add_argument('-i',  type=int, required=False, help='Number of iterations to run', default=1)
    parser.add_argument('--write', action='store_true', required=False, help='Write results to a file (set --t to get a trace)')
    parser.add_argument('--t', action='store_true', required=False, help='Generate and show some trace')
    args = parser.parse_args()
    
    OS = args.o
    if args.o is None:
        OS = linux
    write = args.write
    t = '-X' # -X is not a valid argument and is therefore ignored
    y = '-X'
    if args.t:
        t = "-t0"
        y = "-y"

    time_measurements = []
    my_location_windows = my_location.replace("/", "\\")
    i = 0
    with open(my_location + "/benchmark_trace", 'w') as trace_file:
        while i < args.i:
            i += 1
            output = None
            if write:
                output = trace_file
            
            start = datetime.datetime.now()
            if linux_machine(OS):
                subprocess.Popen([my_location + "verifyta", my_location + 
                    "models/classic_v1.xml", my_location + 
                    "models/classic.q", 
                    "-o1", t, y], stdout=output, stderr=output).wait()
            else:
                subprocess.Popen([my_location_windows + "verifyta.exe", my_location_windows + 
                    "models\\classic_v1.xml", my_location_windows + 
                    "models\\classic.q", 
                    "-o1", t, y], stdout=output, stderr=output).wait()
            end = datetime.datetime.now()
            time = end - start
            total_seconds = time.total_seconds()
            time_measurements.append(total_seconds)
            print(str(i) + ": " + str(time_measurements[-1]))
    print("Avergae time: " + str(sum(time_measurements) / len(time_measurements)))
    