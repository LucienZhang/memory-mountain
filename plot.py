#!/usr/bin/env python

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import sys


def pretty_speed(speed, pos):
    """convert speed to human-readable form.
'speed' is given in bytes.
'pos' is a dummy parameter, required by matplotlib's FuncFormatter.
    """
    suffixes = ['MB/s', 'GB/s']
    unit = 0
    speed = int(speed)  # initially in MB/s
    while speed > 1000:
        speed /= 1000.  # 1000 or 1024 ? cf pretty.c
        unit += 1
    # only keep the decimal part when there is one !
    string = str(speed)
    if string[-2:] == ".0":
        string = string[:-2]
    return string+suffixes[unit]


def pretty_size(logsize, pos):
    """convert size to human-readable form.
'logsize' is the log of the size we want to represent.
'pos' is a dummy parameter, required by matplotlib's FuncFormatter.
"""

    suffixes = ['B', 'kB', 'MB', 'GB']
    unit = 0
    size = int(2**logsize)  # now in bytes
    while size > 1000:
        size /= 1000
        unit += 1
    return f'{size:.2f}{suffixes[unit]}'


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            data = f.read()
    else:
        print("usage: plot.py DATAFILE")
        sys.exit(1)

    data = data.splitlines()

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    fig.set_size_inches(12, 10)

    # stride
    x = np.array([int(row.split(' ')[1]) for row in data])

    # working set size
    y = [int(row.split(' ')[0]) for row in data]
    y = np.log2(y)  # we cheat to get a logarithmic Y axis

    # throughput
    z = np.array([float(row.split(' ')[2]) for row in data])

    ax.plot_trisurf(x, y, z, cmap='rainbow')

    ax.set_xlabel('Stride', labelpad=12)

    ax.set_ylabel('Working set size', labelpad=15)
    ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(pretty_size))
    ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.set_ylim(y.max(), y.min())

    ax.set_zlabel('Throughput', labelpad=15)
    ax.zaxis.set_major_formatter(mpl.ticker.FuncFormatter(pretty_speed))

    plt.savefig('memory_mountain.png', dpi=200)
    plt.show()
