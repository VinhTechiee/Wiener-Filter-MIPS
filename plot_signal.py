import matplotlib.pyplot as plt
import re


def read_signal(file):
    with open(file, "r") as f:
        data = f.read()

    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", data)
    return [float(x) for x in numbers]


def read_output(file):
    with open(file, "r") as f:
        data = f.read()

    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", data)

    filtered = [float(x) for x in numbers[:10]]
    mmse = float(numbers[-1])

    return filtered, mmse


# Load signals
input_signal = read_signal("input.txt")
desired_signal = read_signal("desired.txt")
filtered_signal, mmse = read_output("output.txt")

n = len(input_signal)
x = range(n)

# Compute error signal
error_signal = [desired_signal[i] - filtered_signal[i] for i in range(n)]

# Create figure
fig, axs = plt.subplots(2, 1, figsize=(10, 7))

# ---- Signal comparison ----
axs[0].plot(x, input_signal, marker="o", label="Noisy Input Signal")
axs[0].plot(x, desired_signal, marker="s", label="Desired Signal")
axs[0].plot(x, filtered_signal, marker="^", label="Filtered Output")

axs[0].set_title("Wiener Filter Signal Comparison")
axs[0].set_xlabel("Sample Index")
axs[0].set_ylabel("Amplitude")
axs[0].grid(True)
axs[0].legend()

# ---- Error signal ----
axs[1].plot(x, error_signal, marker="o", color="red")

axs[1].set_title(f"Error Signal (MMSE = {mmse})")
axs[1].set_xlabel("Sample Index")
axs[1].set_ylabel("Error")
axs[1].grid(True)

plt.tight_layout()
plt.savefig("signal_analysis.png", dpi=300)

print("signal_analysis.png generated")