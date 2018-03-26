#Created by Anders!
import subprocess
import argparse
import os
import datetime
import re

my_location = os.path.dirname(os.path.realpath(__file__)) + "/"
linux = 'linux'


def linux_machine(OS_name: str):
    return OS_name == linux

def get_clocks(satID, clock):
    bla = re.findall("(\ p" + satID + "." + clock +"[>]+[=]*[0-9]+)", line)
    if bla:
        return bla[0].split('>')[1]
    else:
        return '0'

def get_delays(first):
    return re.findall("(delays\["+str(first)+"\]\[[0-9]+\]=[0-9]+)", line)

def get_runs(first):
    return re.findall("(runs\["+str(first)+"\]\[[0-9]+\]=[0-9]+)", line)

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
    with open(my_location + "benchmark_trace", 'w') as trace_file:
        while i < args.i:
            i += 1
            output = None
            if write:
                output = trace_file
            p1 = None
            start = datetime.datetime.now()
            if linux_machine(OS):
                subprocess.Popen([my_location + "./verifyta", my_location + "classic_v1.xml", my_location + "classic.q",
                                  "-o1", t, y], stdout=output, stderr=output).wait()
            else:
                subprocess.Popen(my_location_windows + "verifyta.exe -o1 " + t + " " + s + " " + q + " "  + y  + " " + my_location_windows + "classic_v1.xml " + my_location_windows + "classic.q", stdout=output, stderr=output).wait()
            end = datetime.datetime.now()
            time = end - start
            total_seconds = time.total_seconds()
            time_measurements.append(total_seconds)
            print(str(i) + ": " + str(time_measurements[-1]))
    with open('benchmark_trace', 'r') as trace:
        for line in reversed(list(trace)):
            t_time = re.findall("(t_time[>=]+[0-9]+)", line)
            if t_time:
                print("data_earth: " + re.findall("(data_earth\=[0-9]+)", line)[0].split('=')[1])
                print("data_storage: " + re.findall("(data_gathered\=[0-9]+)", line)[0].split('=')[1])
                print('data_internal: ' + re.findall("(data_internal\=[0-9]+)", line)[0].split('=')[1])
                print('satellite one:')

                print('idle clock: ' + get_clocks('0', 'idle'))
                print('wait clock: ' + get_clocks('0', 'wait'))
                print('work clock: ' + get_clocks('0', 'work'))
                print('slew clock: ' + get_clocks('0', 'slew'))
                print('satellite two:')
                print('idle clock: ' + get_clocks('1', 'idle'))
                print('wait clock: ' + get_clocks('1', 'wait'))
                print('work clock: ' + get_clocks('1', 'work'))
                print('slew clock: ' + get_clocks('1', 'slew'))
                print('satellite three:')
                print('idle clock: ' + get_clocks('2', 'idle'))
                print('wait clock: ' + get_clocks('2', 'wait'))
                print('work clock: ' + get_clocks('2', 'work'))
                print('slew clock: ' + get_clocks('2', 'slew'))
                for i in range(0, 3):
                    items = get_delays(i)
                    for item in items:
                        print(item)
                for i in range(0, 3):
                    items = get_runs(i)
                    for item in items:
                        print(item)
                break
    print("Avergae time: " + str(sum(time_measurements) / len(time_measurements)))



