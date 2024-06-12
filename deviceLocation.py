#! /usr/bin/env python3

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------
# constants
#
FIGURE_SIZE = 12

INDENT = '  '
SEPARATOR = 80 * '-'

# ------------------------------------------------------------------------------
# command line arguments
#
parser = argparse.ArgumentParser()
                                                                     # verbosity
parser.add_argument(
    '-v', '--verbose', action='store_true', dest='verbose',
    help = 'verbose console output'
)
                                                                      # log file
parser.add_argument(
    '-f', '--logFile',
    default=os.sep.join([
        os.path.dirname(os.path.realpath(__file__)), 'test.log'
    ]),
    help = 'the GPS log file'
)
                                                  # parse command line arguments
parser_arguments = parser.parse_args()
verbose = parser_arguments.verbose
log_file_spec = parser_arguments.logFile

# ==============================================================================
# Internal functions
#

#-------------------------------------------------------------------------------
# read log file into arrays
#
def read_log():
    time = np.array([])
    latitude = np.array([])
    longitude = np.array([])
    altitude = np.array([])
    log_file = open(log_file_spec, 'r')
    for line in log_file :
        line = line.rstrip("\r\n")
#        print(line)
        parameters = line.split(' ')
        for parameter in parameters :
            (name, value) = parameter.split('=')
            if name.lower() == 'time' :
                time = np.append(time, value)
            elif name.lower() == 'latitude' :
                latitude = np.append(latitude, value)
            elif name.lower() == 'longitude' :
                longitude = np.append(longitude, value)
            elif name.lower() == 'altitude' :
                altitude = np.append(altitude, value)

    return(time, latitude, longitude, altitude)


# ==============================================================================
# Main script
#
                                                               # find IP address
(time, latitude, longitude, altitude) = read_log()
                                                                         # plots
plot_file_spec = '.'.join(log_file_spec.split('.')[:-1]) + '.png'
(fig, ax) = plt.subplots(figsize=(FIGURE_SIZE, FIGURE_SIZE))
ax.plot(longitude, latitude)
ax.plot(longitude, latitude, 'o')
ax.axis('equal')
ax.grid()
plt.savefig(plot_file_spec)
