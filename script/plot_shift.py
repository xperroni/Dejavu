#!/usr/bin/env python

from itertools import count, izip
from math import exp
from os.path import join as joinpath
from sys import float_info

from matplotlib import pyplot, cm

from numpy import array, arange
from numpy import min as amin
from numpy import max as amax
from numpy import sum as asum
from numpy import argmin, argmax


def gaussian(x, sigma):
    p = x ** 2.0
    q = 2.0 * sigma ** 2.0
    return exp(-p / q)


#def attraction(y, g):
#    return argmax([g[i] * gaussian(i - y, 25.0) for i in range(0, len(g))])


def attraction(y, g):
    sum_iw = 0.0
    sum_w = 1.0
    for i in range(0, len(g)):
        w = g[i] * gaussian(i - y, 1.0)
        sum_iw += i * w
        sum_w += w

    return int(round(sum_iw / sum_w))


def shifts(contours):
    estimates = [argmax(contours[0])]
    for attractors in contours[1:]:
        estimates.append(attraction(estimates[-1], attractors))

    return array(estimates) - len(contours[0]) // 2


def plot_contours(plotter, data, x0):
    d = data.T
    (m, n) = d.shape
    c = plotter.matshow(d, cmap=cm.jet, origin='lower', extent=(x0, x0 + n, -m // 2, m // 2))
    pyplot.colorbar(c)


def load_data(folder, x0):
    def load_rows(folder):
        for line in open(joinpath(folder, 'shifts.txt')):
            row = array(eval(line))
            n = amax(row)
            if n > 0:
                yield row / n

    def merge(rows):
        for i in range(x0, len(rows)):
            a = i - x0
            b = i + 1
            row = asum(array(rows[a:b]), 0)
            yield row

    rows = [row for row in load_rows(folder)]
    indices = [int(line) for line in open(joinpath(folder, 'indices.txt'))]

    return (array([row for row in merge(rows)]), indices[x0:])


def plot_ground(plotter, path, x0, indices):
    if path == '':
        return

    def load_ground(path):
        (x, y) = ([], [])
        for line in open(path):
            (x_replay, x_teach, shift) = eval(line)
            x.append(x_replay)
            y.append(shift / 12.0)

        return (array(x), array(y))

    (u, v) = load_ground(path)
    (x, y) = ([], [])
    for (i, k) in izip(indices, count(x0)):
        x.append(k)
        j = argmin((u - i) ** 2.0)
        y.append(v[j])

    plotter.plot(x, y, 'k--')



def plot(x0, folder, ground=''):
    x0 = int(x0)
    (data, indices) = load_data(folder, x0)
    (n, m) = data.shape

    (figure, axes) = pyplot.subplots()
    plot_contours(axes, data, x0)

    d = shifts(data)
    xn = x0 + len(d)

    x = range(x0, xn)
    z = (n - x0)
    axes.plot(x, d, 'k-')

    plot_ground(axes, ground, x0, indices)

    axes.axis([x0, n, -m // 2, m // 2])
    axes.xaxis.set_ticks_position('bottom')
    axes.set_aspect('auto', 'box')

    ticks = arange(x0, n, 50.0)
    axes.set_xticks(ticks)
    axes.set_xticklabels([str(indices[int(i - x0)]) for i in ticks])


    axes.grid()
    axes.set_xlabel('Replay image index #', labelpad=10)
    axes.set_ylabel('Shift (columns)', labelpad=20)

    pyplot.show()


def main():
    from sys import argv
    plot(*argv[1:])


if __name__ == '__main__':
    main()
