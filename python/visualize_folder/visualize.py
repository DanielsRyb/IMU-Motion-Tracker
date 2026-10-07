import matplotlib.pyplot as plt#导入库并命名为plt
#把之前的画图部分写成函数，再导入read_imu.py
def plot_imu_data(
    timestamps,
    accelerations,
    angular_velocities,
    az_values,
    filtered_timestamps_3,
    filtered_az_3,
    filtered_timestamps_5,
    filtered_az_5,
    filtered_timestamps_10,
    filtered_az_10
):
    plt.subplot(3, 1, 1)
    #将画布分成3行，1列，现在作第1幅图
    plt.plot(timestamps, accelerations)#横轴，数轴数据，这里写变量
    plt.xlabel("Time (s)")#横轴标签
    plt.ylabel("Acceleration (m/s²)")#数轴标签
    plt.title("Acceleration vs Time")#图像标题


    plt.subplot(3, 1, 2)
    #将画布分成3行，1列，现在作第2幅图
    plt.plot(timestamps, angular_velocities)
    plt.xlabel("Time (s)")
    plt.ylabel("Angular_velocity (rad/s)")
    plt.title("Angular velocity vs Time")


    plt.subplot(3,1,3)

    plt.plot(timestamps, az_values, label="Raw")#第一条线数据及标签
    plt.plot(filtered_timestamps_3, filtered_az_3, label="MA(3)")#第二条线数据及标签
    plt.plot(filtered_timestamps_5, filtered_az_5, label="MA(5)")#第二条线数据及标签
    plt.plot(filtered_timestamps_10, filtered_az_10, label="MA(10)")#第二条线数据及标签
    plt.xlabel("Time (s)")
    plt.ylabel("az (m/s²)")
    plt.title("z-axis Acceleration vs Time")

    plt.tight_layout() #自动调整三个图之间的间距，避免标题、坐标轴标签互相挤在一起
    plt.legend()
    plt.show()#显示图像




def plot_orientation(timestamps, rolls, pitches):#加速度分析得出
    plt.plot(timestamps, rolls, label = "Roll")
    plt.plot(timestamps, pitches, label = "Pitch")

    plt.xlabel("Time (s)")
    plt.ylabel("Angle (degrees)")
    plt.title("Orientation vs Time")
    plt.legend()

    plt.tight_layout
    plt.show()




def plot_roll_comparison(
    timestamps,
    accelerometer_rolls,
    gyro_rolls,
    filtered_rolls
):
    plt.plot(#第一根线
        timestamps,
        accelerometer_rolls,
        label="Accelerometer"
    )

    plt.plot(#第二根线
        timestamps,
        gyro_rolls,
        label="Gyroscope"
    )

    plt.plot(#第三根线
        timestamps,
        filtered_rolls,
        label="Complementary Filter"
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Roll (degrees)")
    plt.title("Roll Estimation Comparison")
    plt.legend()

    plt.tight_layout()
    plt.show()