#Created by Anders!
import subprocess
import argparse
import os
import datetime
import re

my_location = os.path.dirname(os.path.realpath(__file__)) + "/"

def linux_machine(OS_name: str):
	return OS_name == linux


def get_clocks():
	results = []
	clocks = re.findall("( p[0-9]+.idle[<=]+[0-9]+| p[0-9]+.wait[<=]+[0-9]+| p[0-9]+.work[<=]+[0-9]+| p[0-9]+.slew[<=]+[0-9]+)", line)
	for c in clocks:
		splits = c.split("<=")
		results.append((splits[0].replace(" ", ""), splits[1]))
	return results


def get_delays():
	return re.findall("(delays\[[0-9]+\]\[[0-9]+\]=[0-9]+)", line)


def get_runs():
	return re.findall("(runs\[[0-9]+\]\[[0-9]+\]=[0-9]+)", line)

def write(text, newline=True):
	text = str(text)
	with open('results', 'a') as results:
		if newline:
			text += "\n"
		results.write(text)

if __name__ == '__main__':
	my_location_windows = my_location.replace("/", "\\")

	write(str(datetime.datetime.now()))
	# models
	for model in os.listdir(os.getcwd()):
		i = 0
		count = 0
		splits = model.split('.')
		if len(splits) == 2 and splits[1] == 'xml':
			write(model)
			short_name = splits[0]
			times = []
			with open(my_location + "benchmark_trace", 'w') as trace_file:
				while i < args.i:
					i += 1
					output = None
					if w:
						output = trace_file
					p1 = None
					count += 1
					print("{0} - Current model:{1}".format(count, model))
					start = datetime.datetime.now()
					subprocess.Popen([my_location + "./verifyta", my_location + model, my_location + "classic.q","-o1", "-t0", "y"], stdout=output, stderr=output).wait()
					end = datetime.datetime.now()
					time = end - start
					total_seconds = time.total_seconds()
					write("{0}".format(total_seconds))
					print("Done:{0}".format(model))
			with open('benchmark_trace', 'r') as trace:
				for line in reversed(list(trace)):
					t_time = re.findall("(t_time[>=]+[0-9]+)", line)
					price = re.findall("(band_cost\=[0-9]+)", line)
					if t_time and price:
						price = price[0].split('=')[1]
						write("{0}".format(price))
						earth = re.findall("(data_earth\=[0-9]+)", line)[0].split('=')[1]
						storage = re.findall("(data_gathered\=[0-9]+)", line)[0].split('=')[1]
						internal = re.findall("(data_internal\=[0-9]+)", line)[0].split('=')[1]
						write(earth)
						write(storage)
						write(internal)
						clocks_str = short_name
						for i, clock in enumerate(get_clocks()):
							write("{0}".format(clock[1]))
						for index, d in enumerate(get_delays()):
							d = d.replace("=", "\t").split("\t")[1]
							write("{0}".format(d)) # delays[0][1]=15
						for index, r in enumerate(get_runs()):
							r = r.replace("=", "\t").split("\t")[1]
							write("{0}".format(r))
						break
				write("\n")




#r[0][0]			r[1][0]			r[2][]
#r[0][1]			r[1][1]			...
#...
#d[0][]0 ...
#...
#idle0			idle1			idle2
#wait..
#work...
#slew...
#time	cost	data_earth	data_gathered	data_trans