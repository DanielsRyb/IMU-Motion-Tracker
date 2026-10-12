import numpy as np#NumPy 是 Python 中专门用来处理数字、数组和数学计算的一个库。


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
    ax, ay, az = generate_accelerometer_data(true_roll)


    print("Number of samples:", len(timestamps))
    print("Initial roll:", true_roll[0])
    print("Maximum roll:", np.max(true_roll))
    print("Final roll:", true_roll[-1])
    print("Maximum wx (rad/s):", np.max(wx))
    print("Minimum wx (rad/s):", np.min(wx))
    print("Maximum |wy| (rad/s):", np.max(np.abs(wy)))
    print("Maximum |wz| (rad/s):", np.max(np.abs(wz)))
    print("Initial acceleration:", ax[0], ay[0], az[0])
    print("Acceleration magnitude at start:", np.sqrt(ax[0]**2 + ay[0]**2 + az[0]**2))
    print("Acceleration magnitude at maximum roll:", np.sqrt(ax[np.argmax(true_roll)]**2 + ay[np.argmax(true_roll)]**2 + az[np.argmax(true_roll)]**2))
    acceleration_magnitude = np.sqrt(ax**2 + ay**2 + az**2)

    print("Minimum acceleration magnitude:", np.min(acceleration_magnitude))
    print("Maximum acceleration magnitude:", np.max(acceleration_magnitude))
    print("Maximum magnitude error:", np.max(np.abs(acceleration_magnitude - 9.81)))