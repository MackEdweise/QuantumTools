import math
import csv
import matplotlib.pyplot as plt
import numpy as np
from functools import partial


# constants


GYROMETRIC_RATIO_HYDROGEN = 42.58  # MHz/Tesla
GYROMETRIC_RATIO_HELIUM = -32.43  # MHz/Tesla

INTEGRATION_UPPER_BOUND = 10  # steps long enough to see a few periods of oscillations in Mz
EXPERIMENT_SIMULATION_TIME = 1000

NUCLEAR_MAGNETIZATION_VARS = ['Mx', 'My', 'Mz']


# numerical integrator


def numerically_integrate(f, lower_bound, upper_bound, differential=0.1):
    x = lower_bound
    s = 0
    while x <= upper_bound:
        s += f(x) * differential
        x += differential
    return s


# Bloch equations


def dMx_dt(gyromagnetic_ratio, My, larmor_freq, t):
    return gyromagnetic_ratio * My * larmor_freq


def dMy_dt(gyromagnetic_ratio, Mz, Mx, omega, rf_freq, larmor_freq, t):
    return gyromagnetic_ratio * 2 * Mz * rf_freq * math.cos(omega * t) \
           - gyromagnetic_ratio * Mx * larmor_freq


def dMz_dt(gyromagnetic_ratio, My, omega, rf_freq, t):
    return - gyromagnetic_ratio * 2 * My * rf_freq * math.cos(omega * t)


bloch_equations = [
    dMx_dt,
    dMy_dt,
    dMz_dt
]


# initial conditions


M0 = 0.0000000001  # initial steady state nuclear magnetization vector is small
rf_freq = 0.0001
rf_ratio = 50

Mz = M0
My = 0
Mx = 0

omega = rf_ratio * rf_freq
larmor_freq = omega


# calculations


t = 0
times = []

results = {
    'Mx': [],
    'My': [],
    'Mz': []
}

while t < EXPERIMENT_SIMULATION_TIME:

    dMx = numerically_integrate(
        f=partial(dMx_dt, GYROMETRIC_RATIO_HYDROGEN, My, larmor_freq),
        lower_bound=t,
        upper_bound=t + INTEGRATION_UPPER_BOUND
    )

    dMy = numerically_integrate(
        f=partial(dMy_dt, GYROMETRIC_RATIO_HYDROGEN, Mz, Mx, omega, rf_freq, larmor_freq),
        lower_bound=t,
        upper_bound=t + INTEGRATION_UPPER_BOUND
    )

    dMz = numerically_integrate(
        f=partial(dMz_dt, GYROMETRIC_RATIO_HYDROGEN, My, omega, rf_freq),
        lower_bound=t,
        upper_bound=t + INTEGRATION_UPPER_BOUND
    )

    Mx += dMx
    My += dMy
    Mz += dMz

    results['Mx'].append(Mx)
    results['My'].append(My)
    results['Mz'].append(Mz)

    t += INTEGRATION_UPPER_BOUND
    times.append(t)


# saving results


with open(f'output_{rf_freq}_{rf_ratio}.csv', mode='w+') as output_file:

    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['time'] + NUCLEAR_MAGNETIZATION_VARS)

    i = 0
    while i < EXPERIMENT_SIMULATION_TIME/INTEGRATION_UPPER_BOUND:
        writer.writerow([
            i * INTEGRATION_UPPER_BOUND,
            results[NUCLEAR_MAGNETIZATION_VARS[0]][i],
            results[NUCLEAR_MAGNETIZATION_VARS[1]][i],
            results[NUCLEAR_MAGNETIZATION_VARS[2]][i]
        ])
        i += 1


# plotting results


for var in NUCLEAR_MAGNETIZATION_VARS:
    times = np.arange(0, EXPERIMENT_SIMULATION_TIME, INTEGRATION_UPPER_BOUND)
    curve = results[var]

    fig, ax = plt.subplots()
    ax.plot(times, curve)

    ax.set(xlabel='time', ylabel=var,
           title=f'{var}(t), omega_R = {rf_freq}, omega_0/omega_R = {rf_ratio}')
    ax.grid()
    fig.savefig(f'{var}_{rf_freq}_{rf_ratio}.png')
    plt.show()
