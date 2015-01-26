#!/usr/bin/env python

from math import exp
from sys import float_info

from matplotlib import pyplot, cm

from numpy import array, arange
from numpy import min as amin
from numpy import max as amax
from numpy import sum as asum
from numpy import argmax


def gaussian(x, sigma):
    p = x ** 2.0
    q = 2.0 * sigma ** 2.0
    return exp(-p / q)


def attraction(y, g):
    #return argmax([g[i] * gaussian(i - y, 25.0) for i in range(0, len(g))])

    sum_iw = 0.0
    sum_w = 0.0
    for i in range(0, len(g)):
        w = g[i] * gaussian(i - y, 2.0)
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


def load_data(path, x0):
    def load_rows(path):
        for line in open(path):
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

    rows = [row for row in load_rows(path)]
    return array([row for row in merge(rows)])


def plot_ground(plotter, ground, x0, xn):
    if ground == '':
        return

    (x, y) = ([], [])
    for line in open(ground):
        (x_replay, x_teach, shift) = eval(line)
        if x_replay < x0:
            continue

        if x_replay >= xn:
            break

        x.append(x_replay)
        y.append(shift)

    plotter.plot(x, y, 'w--')



def plot(x0, path, ground=''):
    x0 = int(x0)
    data = load_data(path, x0)
    (n, m) = data.shape

    (figure, axes) = pyplot.subplots()
    plot_contours(axes, data, x0)

    d = shifts(data)
    xn = x0 + len(d)
    print xn

    x = range(x0, xn)
    z = (n - x0)
    axes.plot(x, d, 'k--')

    plot_ground(axes, ground, x0, xn)

    axes.axis([x0, n, -m // 2, m // 2])
    axes.xaxis.set_ticks_position('bottom')
    axes.set_aspect('auto', 'box')

    axes.grid()
    axes.set_xlabel('Replay image index #', labelpad=10)
    axes.set_ylabel('Shift (pixels)', labelpad=20)

    pyplot.show()


def main():
    from sys import argv
    plot(*argv[1:])


if __name__ == '__main__':
    main()
