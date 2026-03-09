import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def read_signal(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", data)
    return [float(x) for x in numbers]


def read_output(file_path, signal_length):
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()

    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", data)
    values = [float(x) for x in numbers]

    if len(values) < signal_length + 1:
        raise ValueError("output.txt does not contain enough values for filtered signal + MMSE.")

    filtered_signal = values[:signal_length]
    mmse = values[-1]
    return filtered_signal, mmse


# -----------------------------
# Load data
# -----------------------------
input_signal = read_signal("input.txt")
desired_signal = read_signal("desired.txt")

n = min(len(input_signal), len(desired_signal))
input_signal = input_signal[:n]
desired_signal = desired_signal[:n]

filtered_signal, mmse = read_output("output.txt", n)

x = list(range(n))
y_min = min(min(input_signal), min(desired_signal), min(filtered_signal)) - 0.5
y_max = max(max(input_signal), max(desired_signal), max(filtered_signal)) + 0.5

# -----------------------------
# Create figure
# -----------------------------
fig, ax = plt.subplots(figsize=(10, 5))

line_input, = ax.plot([], [], marker="o", linewidth=2, label="Noisy Input Signal")
line_desired, = ax.plot([], [], marker="s", linewidth=2, label="Desired Signal")
line_filtered, = ax.plot([], [], marker="^", linewidth=2, label="Filtered Output")

info_text = ax.text(
    0.02, 0.95, "", transform=ax.transAxes,
    fontsize=10, verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)

ax.set_xlim(0, n - 1)
ax.set_ylim(y_min, y_max)
ax.set_xlabel("Sample Index")
ax.set_ylabel("Amplitude")
ax.set_title("Wiener Filter Signal Animation")
ax.grid(True, alpha=0.3)
ax.legend(loc="lower right")


def init():
    line_input.set_data([], [])
    line_desired.set_data([], [])
    line_filtered.set_data([], [])
    info_text.set_text("")
    return line_input, line_desired, line_filtered, info_text


def update(frame):
    """
    Animation plan:
    - Frames 0..n-1: reveal noisy input
    - Frames n..2n-1: reveal desired signal
    - Frames 2n..3n-1: reveal filtered output
    - Final frame: show MMSE summary
    """
    if frame < n:
        k = frame + 1
        line_input.set_data(x[:k], input_signal[:k])
        line_desired.set_data([], [])
        line_filtered.set_data([], [])
        info_text.set_text("Stage: Noisy input signal")
    elif frame < 2 * n:
        k = frame - n + 1
        line_input.set_data(x, input_signal)
        line_desired.set_data(x[:k], desired_signal[:k])
        line_filtered.set_data([], [])
        info_text.set_text("Stage: Desired signal")
    elif frame < 3 * n:
        k = frame - 2 * n + 1
        line_input.set_data(x, input_signal)
        line_desired.set_data(x, desired_signal)
        line_filtered.set_data(x[:k], filtered_signal[:k])
        info_text.set_text("Stage: Filtered output estimation")
    else:
        line_input.set_data(x, input_signal)
        line_desired.set_data(x, desired_signal)
        line_filtered.set_data(x, filtered_signal)
        info_text.set_text(
            f"Stage: Final comparison\n"
            f"MMSE = {mmse}\n"
            f"Samples = {n}"
        )

    return line_input, line_desired, line_filtered, info_text


total_frames = 3 * n + 10

anim = FuncAnimation(
    fig,
    update,
    init_func=init,
    frames=total_frames,
    interval=500,
    blit=False,
    repeat=False
)

anim.save("wiener_filter_animation.gif", writer=PillowWriter(fps=2))
plt.close(fig)

print("Generated: wiener_filter_animation.gif")