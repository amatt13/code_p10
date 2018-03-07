import subprocess
import argparse
import os
import datetime
import re

my_location = os.path.dirname(os.path.realpath(__file__)) + '/'
linux = 'linux'


def linux_machine(OS_name: str):
    return OS_name == linux


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Benchmark tool for UPPAAL models')
    parser.add_argument('-o', type=str, required=False, help='OS name')
    parser.add_argument('-i', type=int, required=False, help='Number of iterations to run', default=1)
    parser.add_argument('--write', action='store_true', required=False, help='Write results to a file (set --t to get a trace)')
    parser.add_argument('--t', action='store_true', required=False, help='Generate and show some trace')
    parser.add_argument('--s', action='store_true', required=False, help='Reduces output')
    args = parser.parse_args()

    OS = args.o
    if args.o is None:
        OS = linux
    write = args.write
    t = y = s = q = ""

    if args.t:
        t = "-t0"
        y = "-y"
    if args.s:
        s = "-s"
        q = "-q"

    time_measurements = []
    my_location_windows = my_location.replace("/", "\\")
    i = 0
    with open(my_location + "/benchmark_trace", 'w') as trace_file:
        while i < args.i:
            i += 1
            output = None
            if write:
                output = trace_file
            p1 = None
            start = datetime.datetime.now()
            if linux_machine(OS):
                subprocess.Popen([my_location + "verifyta", my_location + "models/final_models/classic_v1.xml", my_location + "models/final_models/classic.q",
                    "-o1", t, y, s, q], stdout=output, stderr=output).wait()
            else:
                subprocess.Popen(my_location_windows + "verifyta.exe -o1 " + t + " " + s + " " + q + " "  + y  + " " + my_location_windows + "models\\final_models\\classic_v1.xml " + my_location_windows + "models\\final_models\\classic.q", stdout=output, stderr=output).wait()
            end = datetime.datetime.now()
            time = end - start
            total_seconds = time.total_seconds()
            time_measurements.append(total_seconds)
            print(str(i) + ": " + str(time_measurements[-1]))
    with open('benchmark_trace', 'r') as trace:
        line = trace.readline()
        while line:
            t_time = re.findall("(t_time[>=]+[0-9]+)", line)
            if t_time:
                t_time = t_time[0].split('=')[1]
                if int(t_time) == 597 or int(t_time) == 600:
                    print("data_earth: " + re.findall("(data_earth\=[0-9]+)", line)[0].split('=')[1])
                    print("data_storage: " + re.findall("(data_storage\=[0-9]+)", line)[0].split('=')[1])
                    print('internal_transfer: ' + re.findall("(internal_transfer\=[0-9]+)", line)[0].split('=')[1])
            line = trace.readline()
    print("Avergae time: " + str(sum(time_measurements) / len(time_measurements)))
