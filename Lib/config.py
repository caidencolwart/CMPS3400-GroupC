import os

OUTPUT_DIR = os.path.join("Output")
LOG_DIR = os.path.join(OUTPUT_DIR, "logs")
PLOT_DIR = os.path.join(OUTPUT_DIR, "plots")

for d in [OUTPUT_DIR, LOG_DIR, PLOT_DIR]:
    os.makedirs(d, exist_ok=True)