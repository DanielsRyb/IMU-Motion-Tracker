import numpy as np#NumPy 是 Python 中专门用来处理数字、数组和数学计算的一个库。
import matplotlib.pyplot as plt
from filters.adaptive_complementary import (
    calculate_acceleration_magnitude,
    calculate_alpha,
    adaptive_complementary_filter,
)

#生成数据的思路：先规定转动角度数据的函数，然后再求它对时间的导数得出角速度，接着再正交分解得到在x,y,z上的分量
def generate_true_roll(timestamps):
    """
    Generate a smooth ground-truth roll trajectory.
    0-2 s:  roll from 0 to 30 degrees
    2-4 s:  roll from 30 to 0 degrees
    4-6 s:  remain at 0 degrees
    """#三重双引号作标注

    roll_degrees = np.zeros_like(timestamps, dtype=float)#创建一个与时间戳数组长度相同的数组，并将所有角度初始化为 0°

    # 0-30
    mask_up = (timestamps >= 0) & (timestamps < 2)#布尔函数，取timestamps数组里面>=0,<2的部份设为True，其余不符条件的为 False
    u_up = timestamps[mask_up] / 2#取timestamps里面mask_up对应位置为True 的元素，每一项除以2，Vectorized Operation
    #归一化时间，把一段时间按比例缩放到 0～1 之间
    roll_degrees[mask_up] = 30 * (
        3 * u_up**2 - 2 * u_up**3#s(u)=30*(3u^2-2u^3)，导函数在u=0点和u=1处为0，数据平滑无突变，陀螺仪测量角速度不会有突变
    )#离散的时间数组里面，只要数据长度对齐就行，不必再代回原本的时间戳尺度

    # 30-0
    mask_down = (timestamps >= 2) & (timestamps < 4)
    u_down = (timestamps[mask_down] - 2) / 2

    roll_degrees[mask_down] = 30 * (
        1 - 3 * u_down**2 + 2 * u_down**3#s(u)=30*(1-3u^2+2u^3)
    )

    # 0
    return roll_degrees

def generate_gyro_data(timestamps, roll_degrees):
    """
    Generate ideal gyroscope data for pure roll motion.
    Returns angular velocity in rad/s.
    """

    # degrees to radians
    roll_radians = np.deg2rad(roll_degrees)

    # Calculate angular velocity
    wx = np.gradient(roll_radians, timestamps)#np.gradient(x, t)用于数值求导，头尾以外的数值用中心差分，即取前后两个数值的差求导

    # No rotation around Y and Z axes in this experiment
    wy = np.zeros_like(wx)
    wz = np.zeros_like(wx)

    return wx, wy, wz


def generate_accelerometer_data(roll_degrees):#由角度得出重力分量
    """
    Generate ideal accelerometer data for pure roll motion.

    Assumptions:
    - No linear acceleration
    - Gravity magnitude is 9.81 m/s^2
    - Coordinate signs are consistent with calculate_roll()
    """

    gravity = 9.81

    # degrees to radians
    roll_radians = np.deg2rad(roll_degrees)

    # Gravity components in the sensor coordinate frame
    ax = np.zeros_like(roll_radians)
    ay = gravity * np.sin(roll_radians)
    az = gravity * np.cos(roll_radians)

    return ax, ay, az


if __name__ == "__main__":
    sample_rate = 100
    duration = 6
    timestamps = np.arange(0, duration, 1 / sample_rate)#生成数组：起点为0，步长为0.01，终点到6，一般不包含终点

    true_roll = generate_true_roll(timestamps)

    wx, wy, wz = generate_gyro_data(timestamps, true_roll)
    # Add a constant gyroscope bias
    gyro_bias = np.deg2rad(0.5)  # 0.5 degrees per second
    wx = wx + gyro_bias


    ax, ay, az = generate_accelerometer_data(true_roll)
    # Add Gaussian noise to accelerometer measurements
    acc_noise_std = 0.05  # m/s^2

    ax = ax + np.random.normal(0, acc_noise_std, size=ax.shape)
    ay = ay + np.random.normal(0, acc_noise_std, size=ay.shape)
    az = az + np.random.normal(0, acc_noise_std, size=az.shape)


    # Reconstruct roll angle by integrating gyroscope data
    dt = timestamps[1] - timestamps[0]

    roll_from_gyro = np.zeros_like(true_roll)

    for i in range(1, len(timestamps)):
        roll_from_gyro[i] = (
            roll_from_gyro[i - 1] + np.rad2deg(wx[i] * dt)
        )

    # Calculate estimation error
    gyro_error = roll_from_gyro - true_roll

    print("Maximum absolute gyro error (degrees):",
      np.max(np.abs(gyro_error)))




    # Reconstruct roll angle from accelerometer data
    roll_from_acc = np.rad2deg(np.arctan2(ay, az))

    # Calculate estimation error
    roll_error = roll_from_acc - true_roll

    print("Maximum absolute roll error (degrees):",
        np.max(np.abs(roll_error)))     



    # Calculate root mean square error (RMSE)
    gyro_rmse = np.sqrt(np.mean(gyro_error**2))
    acc_rmse = np.sqrt(np.mean(roll_error**2))

    print("Gyroscope RMSE (degrees):", gyro_rmse)
    print("Accelerometer RMSE (degrees):", acc_rmse)
    #Gyroscope errors primarily stem from discretization errors in numerical differentiation and integration.



    # Apply complementary filter
    alpha = 0.98
    roll_from_complementary = np.zeros_like(true_roll)

    for i in range(1, len(timestamps)):
        gyro_angle = (roll_from_complementary[i - 1] + np.rad2deg(wx[i] * dt))

        roll_from_complementary[i] = (alpha * gyro_angle + (1 - alpha) * roll_from_acc[i])#0.98*gyro + 0.02*acc

    # Calculate complementary filter error
    complementary_error = roll_from_complementary - true_roll
    complementary_rmse = np.sqrt(np.mean(complementary_error**2))

    print("Complementary filter RMSE (degrees):", complementary_rmse)


    # Check acceleration magnitude deviation
    acceleration_magnitude = np.sqrt(ax**2 + ay**2 + az**2)
    acceleration_deviation = np.abs(acceleration_magnitude - 9.81)

    print("Maximum acceleration magnitude deviation (m/s^2):", np.max(acceleration_deviation))


    # Apply adaptive complementary filter
    roll_from_adaptive = np.zeros_like(true_roll)
    alpha_values = np.zeros_like(true_roll)

    for i in range(1, len(timestamps)):
        # Calculate acceleration magnitude
        acc_magnitude = calculate_acceleration_magnitude(
            ax[i], ay[i], az[i]
        )

        # Adapt alpha according to acceleration magnitude
        alpha = calculate_alpha(acc_magnitude)
        alpha_values[i] = alpha

        # Update roll estimate
        roll_from_adaptive[i] = adaptive_complementary_filter(
            roll_from_adaptive[i - 1],
            wx[i],
            dt,
            roll_from_acc[i],
            alpha,
        )

    # Calculate adaptive filter error and RMSE
    adaptive_error = roll_from_adaptive - true_roll
    adaptive_rmse = np.sqrt(np.mean(adaptive_error**2))

    print("Adaptive complementary filter RMSE (degrees):",
        adaptive_rmse)
    print("Minimum alpha:", np.min(alpha_values[1:]))
    print("Maximum alpha:", np.max(alpha_values[1:]))



    # Plot roll angle estimates
    plt.figure(figsize=(10, 5))

    plt.plot(timestamps, true_roll, label="True roll")
    plt.plot(timestamps, roll_from_gyro, label="Gyroscope")
    plt.plot(timestamps, roll_from_acc, label="Accelerometer")
    plt.plot(timestamps, roll_from_complementary, label="Complementary filter")

    plt.xlabel("Time (s)")
    plt.ylabel("Roll angle (degrees)")
    plt.title("Roll Angle Estimation Comparison")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot estimation errors
    plt.figure(figsize=(10, 5))

    plt.plot(timestamps, gyro_error, label="Gyroscope error")
    plt.plot(timestamps, roll_error, label="Accelerometer error")
    plt.plot(timestamps, complementary_error, label="Complementary filter error")
    plt.plot(timestamps, adaptive_error, label="Adaptive complementary filter error")

    plt.xlabel("Time (s)")
    plt.ylabel("Error (degrees)")
    plt.title("Roll Angle Estimation Errors")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()