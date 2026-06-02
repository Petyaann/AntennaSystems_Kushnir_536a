import numpy as np
import matplotlib.pyplot as plt
import math

variant = 12
lambd = 0.031
N = 6
l_slot = 0.016
d = 0.032
lambd_w = 2 * d
level = 0.707

theta_deg = np.arange(-90, 90, 0.01)
theta = np.radians(theta_deg)

k = 2 * math.pi / lambd

psi_E = k * d * np.sin(theta) - (2 * math.pi * d / lambd_w)
den_E = N * np.sin(psi_E / 2)

Fc_E = np.where(abs(den_E) < 1e-8, 1, abs(np.sin(N * psi_E / 2) / den_E))
F1_E = abs(np.cos(theta))
FE = abs(F1_E * Fc_E)

psi_H = k * d * np.sin(theta) + (2 * math.pi * d / lambd_w)
den_H = N * np.sin(psi_H / 2)

Fc_H = np.where(abs(den_H) < 1e-8, 1, abs(np.sin(N * psi_H / 2) / den_H))
F1_H = 1
FH = abs(F1_H * Fc_H)

FE = FE / max(FE)
FH = FH / max(FH)


def get_width(F):
    max_index = np.argmax(F)

    left = 0
    right = 0

    for i in range(max_index, 0, -1):
        if F[i] < level:
            left = theta_deg[i]
            break

    for i in range(max_index, len(F)):
        if F[i] < level:
            right = theta_deg[i]
            break

    return abs(right - left), left, right


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
    width, left, right = get_width(F)

    print(f"--- {name} ---")

    print("Табл. 1 - Значення нульових кутів")
    print("| № |   θ   | F(θ) |")
    for i, (x, y) in enumerate(zip(min_x, min_y), 1):
        print(f"| {i} | {x:6.2f} | {y:5.2f} |")

    print()

    print("Табл. 2 - Значення максимальних кутів")
    print("| № |   θ   | F(θ) |")
    for i, (x, y) in enumerate(zip(max_x, max_y), 1):
        print(f"| {i} | {x:6.2f} | {y:5.2f} |")

    print(f"\nЛіва точка рівня 0.707 = {left:.2f}°")
    print(f"Права точка рівня 0.707 = {right:.2f}°")
    print(f"Ширина головної пелюстки = {width:.2f}°\n")


print(f"Варіант = {variant}")
print(f"Довжина хвилі = {lambd} (м)")
print(f"Тип антени = поперечні щілини у широкій стінці хвилеводу")
print(f"Кількість щілин N = {N}")
print(f"Довжина щілини l = {l_slot} (м)")
print(f"Відстань між щілинами d = {d} (м)")
print(f"Довжина хвилі у хвилеводі λхв = {lambd_w} (м)\n")

print_table("Хвилеводно-щілинна антена, площина E", FE)
print_table("Хвилеводно-щілинна антена, площина H", FH)

plt.figure("Хвилеводно-щілинна антена E", figsize=(10, 6))
plt.plot(theta_deg, FE, label=r"$F_E(\theta)$")
plt.axhline(level, color="red", linestyle="--")
plt.grid(True)
plt.xlabel(r"$\Theta^{\circ}$")
plt.ylabel(r"$|F_E(\theta)|$")
plt.title("ДС хвилеводно-щілинної антени у площині E")
plt.legend()

plt.figure("Хвилеводно-щілинна антена H", figsize=(10, 6))
plt.plot(theta_deg, FH, label=r"$F_H(\theta)$")
plt.axhline(level, color="red", linestyle="--")
plt.grid(True)
plt.xlabel(r"$\Theta^{\circ}$")
plt.ylabel(r"$|F_H(\theta)|$")
plt.title("ДС хвилеводно-щілинної антени у площині H")
plt.legend()

plt.show()