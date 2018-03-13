import ephem
import datetime
import numpy as np
from math import atan2

RADIUS_EARTH = 6.37 * 10 ** 6
# Newton's Law - universal gravitation constant
G = 6.673 * 10 ** -11


class Orbit:
    def __init__(self, inclination, RAAN, eccentricity, aPerigee, mAnomaly, mMotion, revolutionAtEpoch):
        self.inclination = inclination
        self.RAAN = RAAN
        self.eccentricity = eccentricity
        self.aPerigee = aPerigee
        self.mAnomaly = mAnomaly
        self.mMotion = mMotion
        self.revolutionAtEpoch = revolutionAtEpoch


class Station:
    def __init__(self, longitude, latitude, distance):
        self.longitude = longitude
        self.latitude = latitude
        self.distance = distance


def checksum(line: str):
    checksum = 0
    for x in line:
        if x.isdigit() and int(x) != 0:
            checksum = checksum + int(x)
        elif x == "-":
            checksum = checksum + 1
    return line + str(checksum)[-1]


# line 1
# 1     - Line Number of Element Data
# 3-7   - Satellite Number
# 8     - Classification
# 10-11 - International Designator (Last two digits of launch year)
# 12-14 - International Designator (Launch number of the year)
# 15-17 - International Designator (Piece of the launch)
# 19-20 - Epoch Year (Last two digits of year)
# 21-32 - Epoch (Day of the year and fractional portion of the day)
# 34-43 - First Time Derivative of Mean Motion
# 45-52 - Second Time Derivative of Mean Motion (decimal point assumed)
# 54-61 - BSTAR drag term (decimal point assumed)
# 63    - Ephemeris type
# 65-68 - Element number
# 69    - Checksum
def construct_line_one(year, days):
    c1 = "1"
    c3_7 = "99999"
    c8 = " "
    c10_11 = "18"
    c12_14 = "100"
    c15_17 = "A  "
    c19_20 = str(year)
    c21_32 = str(days)
    if len(str(days).split(".")[0]) != 3:
        c21_32 = "0" + c21_32
    if len(str(c21_32)) > 12:
        c21_32 = c21_32[:12]
    else:
        for x in range(12 - len(str(c21_32))):
            c21_32 = c21_32 + "0"
    c34_43 = "0.00001906"
    c45_52 = "49422-5"
    c54_61 = "00000+0"
    c63 = "0"
    c65_68 = "999"
    line1 = "{0} {1}{2} {3}{4}{5} {6}{7} {8} {9}  {10}  {11}  {12}".format(c1, c3_7, c8, c10_11, c12_14, c15_17, c19_20,
                                                                           c21_32,
                                                                           c34_43, c45_52, c54_61, c63, c65_68)
    return checksum(line1)


# line 2
# 1     - Line Number of  Element Data
# 3-7   - Satellite Number
# 9-16  - Inclination [Degrees]
# 18-25 - Right Ascension of the Ascending Node [Degrees]
# 27-33 - Eccentricity (decimal point assumed)
# 35-42 - Argument of Perigee [Degrees]
# 44-51 - Mean Anomaly [Degrees]
# 53-63 - Mean Motion [Revs per day]
# 64-68 - Revolution number at epoch [Revs]
# 69    - Checksum
def construct_line_two(inclination, RAAN, eccentricity, aPerigee, mAnomaly, mMotion, revolutionAtEpoch):
    b = " "
    c1 = "2"
    c3_7 = "99999"
    c9_16 = str(inclination)
    c18_25 = str(RAAN)
    c27_33 = str(eccentricity)
    c35_42 = str(aPerigee)
    c44_51 = str(mAnomaly)
    c53_63 = str(mMotion)
    c64_68 = str(revolutionAtEpoch)
    line2 = "{0} {1}  {2}  {3} {4}  {5}  {6} {7}{8}".format(c1, c3_7, c9_16, c18_25, c27_33, c35_42, c44_51, c53_63,
                                                            c64_68)
    return checksum(line2)


def calculate_orbit(height_amount):
    radius_orbit = RADIUS_EARTH + height_amount
    # kg
    mass_earth = 5.98 * 10 ** 24
    # Orbital Speed Equations
    v = np.math.sqrt((G * mass_earth) / radius_orbit)
    # Acceleration Equation
    a = (G * mass_earth) / radius_orbit ** 2
    # Orbital Period Equation
    t = np.math.sqrt((4 * (np.math.pi ** 2) * (radius_orbit ** 3)) / (G * mass_earth))
    print("Base Properties:")
    print("Universal Gravitation Constant", G)
    print("Earth's Radius", RADIUS_EARTH)
    print("Orbital Height", height_amount)
    print("Orbital Radius", radius_orbit)
    print("Earth's mass", mass_earth)

    print("Orbit Properties:")
    print("Orbital speed", v)
    print("Acceleration", a)
    print("Orbital Period", t / 60)
    return [v, a, t / 60]


# line2 = construct_line_two("50.0000", "020.519", "0020247", "81.2115", "279.186", "16.30050059", "00000")
def generate_data_for_station(stations, orbit, schedule_length, list):
    LL = []
    returnset = []
    date = datetime.datetime(2018, 3, 7, 9, 40, 39)
    for x in range(0, schedule_length, 1):
        day_of_year = date.timetuple().tm_yday + (date.hour + ((date.minute + x) / 60)) / 24
        date_only = str(date).split(" ")[0].replace("-", "/")
        date_year = str(date).split("-")[0]
        line1 = construct_line_one(str(date_year)[2:], day_of_year)
        line2 = construct_line_two(orbit.inclination, orbit.RAAN, orbit.eccentricity, orbit.aPerigee, orbit.mAnomaly,
                                   orbit.mMotion, orbit.revolutionAtEpoch)
        tle = ephem.readtle("OrbitName", line1, line2)
        tle.compute(date_only)
        lat = float(str(tle.sublat).split(":")[-3]) + float(str(tle.sublat).split(":")[-2]) / 60 + float(
            str(tle.sublat).split(":")[-1]) / (60 * 60)
        long = float(str(tle.sublong).split(":")[-3])
        if long < 0:
            long += (float(str(tle.sublong).split(":")[-2]) / 60 + float(str(tle.sublong).split(":")[-1]) / (
                60 * 60)) * -1
        else:
            long += float(str(tle.sublong).split(":")[-2]) / 60 + float(str(tle.sublong).split(":")[-1]) / (
                60 * 60)
        LL.append([long, lat])
    for sta in stations:
        set = []
        for y in LL:
            lat1 = np.radians(sta.latitude)
            lon1 = np.radians(sta.longitude)
            lat2 = np.radians(y[1])
            lon2 = np.radians(y[0])

            dlon = np.radians(lon2 - lon1)
            dlat = np.radians(lat2 - lat1)
            a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
            c = 2 * atan2(np.sqrt(a), np.sqrt(1 - a))

            distance = RADIUS_EARTH * c
            if distance >= sta.distance:
                set.append(0)
            else:
                set.append(1)
        list.append(set)


def format_data(array):
    output = 'const int OVER_STATION[STATION_INDEX][STATIONS][STATION_ATTRI] = {\n'
    complete_set = []
    for lists, aValue in enumerate(array):
        first = array[lists][0]
        count = 0
        dataset = []
        for index, value in enumerate(array[lists]):
            if value == first:
                count += 1
            else:
                dataset.append([index - count, index, first, lists])
                count = 0
                first = value
        dataset.append([len(array[lists]) - count, len(array[lists]), first, lists])
        complete_set.append(dataset)
    longest = 0
    number_of_lists = 0
    x1 = 0
    x2 = 0
    for i, v in enumerate(complete_set):
        number_of_lists += 1
        if len(complete_set[i]) > longest:
            longest = len(complete_set[i])
    for i in range(longest):
        output += '{'
        for x in range(number_of_lists):
            if len(complete_set[x]) > i:
                output += '{' + str(complete_set[x][i][0]) + ', ' + str(complete_set[x][i][1]) + ', ' + str(
                    complete_set[x][i][2]) + '}, '
            else:
                output += '{0, 9999, 0}, '
        output = output[:-2]
        output += '},\n'
        x2 += 1
    output = output[:-2]
    output += '};'
    print('const int STATION_INDEX = ' + str(x2) + '; // changes for; when station are in range')
    print('const int STATIONS = ' + str(len(array)) + '; // amount of windows i.e. stations to which can be communicated')
    print('const int STATION_ATTRI = ' + str(3) + '; // elements discribing window')
    print('// Start_time, End_time, active or not')
    print(output)


if __name__ == '__main__':
    orbit1 = Orbit("50.0000", "020.519", "0020247", "81.2115", "279.186", "16.30050059", "00000")
    orbit2 = Orbit("45.0000", "060.519", "0020247", "79.2115", "260.186", "16.20050059", "00000")
    orbit3 = Orbit("60.0000", "160.519", "0020247", "75.2115", "220.186", "16.40050059", "00000")
    stations = [Station(-45.10, 50.00, 50000), Station(-32.50, 75.00, 10000000), Station(-45.10, 63.25, 75000), Station(-70.60, 20.13, 80000)]
    locations = []
    length = 1440
    generate_data_for_station(stations, orbit1, length, locations)
    format_data(locations)
