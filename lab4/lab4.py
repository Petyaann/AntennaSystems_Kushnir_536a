import numpy as np
import matplotlib.pyplot as plt
import math

variant = 12
lambd = 0.044
h = 0.08
l = 0.237

xi = 1 + lambd / (2 * l)
level = 0.707

theta_deg = np.arange(0, 90, 0.01)
theta = np.radians(theta_deg)

Fb = abs(
    (np.sin((math.pi * l / lambd) * (xi - np.cos(theta))) /
     np.sin((math.pi * l / lambd) * (xi - 1))) *
    ((xi - 1) / (xi - np.cos(theta)))
)

F1_E = abs(Fb * np.cos(theta))
F1_H = abs(Fb)

Fc = abs(np.cos((math.pi * h / lambd) * np.sin(theta)))

F2_E = abs(F1_E * Fc)
F2_H = abs(F1_H * Fc)

F1_E = F1_E / max(F1_E)
F1_H = F1_H / max(F1_H)
F2_E = F2_E / max(F2_E)
F2_H = F2_H / max(F2_H)


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
print(f"Відстань між стрижнями h = {h} (м)")
print(f"Довжина стрижня l = {l} (м)")
print(f"Коефіцієнт уповільнення ξ = {xi:.3f}\n")

print_table("Одно-стрижнева ДСА, площина E", F1_E)
print_table("Одно-стрижнева ДСА, площина H", F1_H)
print_table("Дво-стрижнева ДСА, площина E", F2_E)
print_table("Дво-стрижнева ДСА, площина H", F2_H)

plt.figure("Одно-стрижнева ДСА E", figsize=(10, 6))
plt.plot(theta_deg, F1_E, label=r"$F_E(\theta)$")
plt.axhline(level, color="red", linestyle="--")
plt.grid(True)
plt.xlabel(r"$\Theta^{\circ}$")
plt.ylabel(r"$|F_E(\theta)|$")
plt.title("ДС одно-стрижневої ДСА у площині E")
plt.legend()

plt.figure("Одно-стрижнева ДСА H", figsize=(10, 6))
plt.plot(theta_deg, F1_H, label=r"$F_H(\theta)$")
plt.axhline(level, color="red", linestyle="--")
plt.grid(True)
plt.xlabel(r"$\Theta^{\circ}$")
plt.ylabel(r"$|F_H(\theta)|$")
plt.title("ДС одно-стрижневої ДСА у площині H")
plt.legend()

plt.figure("Дво-стрижнева ДСА E", figsize=(10, 6))
plt.plot(theta_deg, F2_E, label=r"$F_E(\theta)$")
plt.axhline(level, color="red", linestyle="--")
plt.grid(True)
plt.xlabel(r"$\Theta^{\circ}$")
plt.ylabel(r"$|F_E(\theta)|$")
plt.title("ДС дво-стрижневої ДСА у площині E")
plt.legend()

plt.figure("Дво-стрижнева ДСА H", figsize=(10, 6))
plt.plot(theta_deg, F2_H, label=r"$F_H(\theta)$")
plt.axhline(level, color="red", linestyle="--")
plt.grid(True)
plt.xlabel(r"$\Theta^{\circ}$")
plt.ylabel(r"$|F_H(\theta)|$")
plt.title("ДС дво-стрижневої ДСА у площині H")
plt.legend()

plt.show()