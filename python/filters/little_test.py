import math
import matplotlib.pyplot as plt

from filters.complementary_filter_file import complementary_filter
from filters.adaptive_complementary import calculate_acceleration_magnitude, calculate_alpha, adaptive_complementary_filter

sample_rate = 100
duration = 10
dt = 1 / sample_rate

timestamps = []

accelerometer_rolls = []
gyro_rolls = []
fixed_complementary_filtered_rolls = []

alphas = []
adaptive_complementary_filtered_rolls = []


gyro_roll = 0.0
fixed_complementary_filtered_roll = 0.0
adaptive_complementary_filtered_roll = 0.0

for i in range(sample_rate * duration):

    timestamp = i * dt

    wx = 0.0#没有旋转

    ax = 0
    az = 9.81#重力

    if 3 <= timestamp < 5:#出现加速度
        ay = 3.0
    else:
        ay = 0.0

    # Accelerometer roll
    accelerometer_roll = math.atan2(ay, az)

    # Gyroscope integration
    gyro_roll = gyro_roll + wx * dt

    fixed_complementary_filtered_roll = complementary_filter(
        fixed_complementary_filtered_roll,
        wx,
        dt,
        accelerometer_roll
    )


    alpha = calculate_alpha(calculate_acceleration_magnitude(ax, ay, az),
    alpha_normal=0.98,
    alpha_dynamic=0.995,
    threshold=0.025)

    adaptive_complementary_filtered_roll = adaptive_complementary_filter(
    adaptive_complementary_filtered_roll,
    wx,
    dt,
    accelerometer_roll,
    alpha
    )


    timestamps.append(timestamp)
    accelerometer_rolls.append(math.degrees(accelerometer_roll))
    gyro_rolls.append(math.degrees(gyro_roll))
    fixed_complementary_filtered_rolls.append(math.degrees(fixed_complementary_filtered_roll))
    alphas.append(alpha)
    adaptive_complementary_filtered_rolls.append(math.degrees(adaptive_complementary_filtered_roll))


plt.subplot(2, 1, 1)
plt.plot(
    timestamps,
    accelerometer_rolls,
    label="Accelerometer"
)

plt.plot(
    timestamps,
    gyro_rolls,
    label="Gyroscope"
)

plt.plot(
    timestamps,
    fixed_complementary_filtered_rolls,
    label="Fixed Complementary Filter"
)

plt.plot(
    timestamps,
    adaptive_complementary_filtered_rolls,
    label="Adaptive Complementary Filter"
)

plt.xlabel("Time (s)")
plt.ylabel("Roll (degrees)")
plt.title("Fixed vs Adaptive Complementary Filters")


plt.subplot(2, 1, 2)

plt.plot(timestamps, alphas, label="Adaptive Alpha")
plt.xlabel("Time (s)")
plt.ylabel("Alpha")
plt.title("Adaptive Filter Alpha")
plt.subplots_adjust(hspace=0.6)#调整上下间距
plt.show()