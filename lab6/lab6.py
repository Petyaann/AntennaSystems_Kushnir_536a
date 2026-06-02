import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.special import jv

variant = 12
lambd = 0.031
D = 0.7
f = 0.4

R0 = D / 2
p = 2 * f
k = 2 * math.pi / lambd
level = 0.707

theta_deg = np.arange(0, 90, 0.01)
theta = np.radians(theta_deg)

u = k * R0 * np.sin(theta)
v = 3.5 * R0 / p

j1_u_u = np.where(abs(u) < 1e-8, 0.5, jv(1, u) / u)
j1_v_v = jv(1, v) / v

den1 = v ** 2 - u ** 2
den2 = (1.5 * v) ** 2 - u ** 2

part1 = np.where(
    abs(den1) < 1e-8,
    0,
    0.74 * ((v * jv(1, v) * jv(0, u) - u * jv(1, u) * jv(0, v)) / den1)
)

part2 = 0.26 * j1_u_u

part3 = np.where(
    abs(den2) < 1e-8,
    0,
    0.25 * ((u * jv(1, u) * jv(2, 1.5 * v) - 1.5 * v * jv(1, 1.5 * v) * jv(2, u)) / den2)
)

normal = 1 / (0.74 * j1_v_v + 0.13)

FE = abs((np.cos(theta / 2) ** 2) * (part1 + part2 + part3) * normal)
FH = abs((np.cos(theta / 2) ** 2) * (part1 + part2 - part3) * normal)

FE = FE / max(FE)
FH = FH / max(FH)


def get_width(F):
    for i in range(len(F)):
        if F[i] < level:
            return 2 * theta_deg[i]
    return 0


def find_extremes(x, y):
    max_x = []
    max_y = []
    min_x = []
    min_y = []

    for i in range(1, len(y) - 1):
        if y[i] > y[i - 1] and y[i] > y[i + 1]:
            max_x.append(x[i])
            max_y.append(y[i])

        if y[i] < y[i - 1] and y[i] < y[i + 1]:
            min_x.append(x[i])
            min_y.append(0)

    return max_x, max_y, min_x, min_y


def print_table(name, F):
    max_x, max_y, min_x, min_y = find_extremes(theta_deg, F)

    print(f"--- {name} ---")

    print("Табл. 1 - Значення нульових кутів")
    print("| № |   θ   | F(θ) |")
    for i, (x, y) in enumerate(zip(min_x, min_y), 1):
        print(f"| {i} | {x:5.2f} | {y:5.2f} |")

    print()

    print("Табл. 2 - Значення максимальних кутів")
    print("| № |   θ   | F(θ) |")
    for i, (x, y) in enumerate(zip(max_x, max_y), 1):
        print(f"| {i} | {x:5.2f} | {y:5.2f} |")

    print(f"\nШирина головної пелюстки = {get_width(F):.2f}°\n")


print(f"Варіант = {variant}")
print(f"Довжина хвилі = {lambd} (м)")
print(f"Діаметр дзеркала D = {D} (м)")
print(f"Радіус дзеркала R0 = {R0} (м)")
print(f"Фокусна відстань f = {f} (м)")
print(f"Подвоєна фокусна відстань p = {p} (м)")
print(f"Хвильове число k = {k:.2f} рад/м\n")

print_table("Дзеркальна антена, площина E", FE)
print_table("Дзеркальна антена, площина H", FH)

plt.figure("Дзеркальна антена E", figsize=(10, 6))
plt.plot(theta_deg, FE, label=r"$F_E(\theta)$")
plt.axhline(level, color="red", linestyle="--")
plt.grid(True)
plt.xlabel(r"$\Theta^{\circ}$")
plt.ylabel(r"$|F_E(\theta)|$")
plt.title("ДС дзеркальної антени у площині E")
plt.legend()

plt.figure("Дзеркальна антена H", figsize=(10, 6))
plt.plot(theta_deg, FH, label=r"$F_H(\theta)$")
plt.axhline(level, color="red", linestyle="--")
plt.grid(True)
plt.xlabel(r"$\Theta^{\circ}$")
plt.ylabel(r"$|F_H(\theta)|$")
plt.title("ДС дзеркальної антени у площині H")
plt.legend()

plt.show()