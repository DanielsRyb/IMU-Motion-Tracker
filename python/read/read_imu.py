import math
from filters.filter import moving_average#从filter文件里面导入moving_average函数过来
from visualize_folder.visualize import plot_imu_data
from load_data_fodler.load_data import load_imu_data
from analysis_folder.analysis import calculate_std_deviation
from analysis_folder.analysis import response_time_90


timestamps = []#创建一个空list用于后续存储连续的数据以便画图
accelerations = []#注意这里有“s”，以区分列表和后续使用的浮点数
angular_velocities = []
az_values = []




with open("data/simulated.csv", "r") as file:#with...as...打开一个文件并命名
    
    print(f"{'timestamp':>10} {'ax':>8} {'ay':>8} {'az':>8} {'acceleration':>15} {'wx':>8} {'wy':>8} {'wz':>8} {'angular_velocity':>20}")#f"..."表示f-string，引号内用{}可以代入变量
    
    data = load_imu_data("data/simulated.csv")#数据交给load文件，返回data

    print(data[0])

    for row in data:
        ax = row["ax"] 
        ay = row["ay"]
        az = row["az"]

        az_values.append(az)
        acceleration = math.sqrt(ax**2 + ay**2 + az**2)

        timestamps.append(row["timestamp"]) #将当前timestamp加入timestamp列表
        accelerations.append(acceleration)

        wx = row["wx"]
        wy = row["wy"]
        wz = row["wz"]

        angular_velocity = math.sqrt(wx**2 + wy**2 + wz**2)
        angular_velocities.append(angular_velocity)

        print(f"{row['timestamp']:>10} {ax:>8.2f} {ay:>8.2f} {az:>8.2f} {acceleration:>15.2f} {wx:>8.2f} {wy:>8.2f} {wz:>8.2f} {angular_velocity:>20.2f}")


filtered_az_3 = moving_average(az_values, 3)
filtered_az_5 = moving_average(az_values, 5)#窗口为5，相当于用前2个后2个平滑处理当前的值，并且让方差σ变成σ/√5但是会导致最终数据从原本的len(data)个数据减少为(len(data) - window_size + 1)个，需要让时间戳对齐
filtered_az_10 = moving_average(az_values, 10)

filtered_timestamps_3 = timestamps[2:]#casual filter有延迟但是输出时间对应当前时间戳
filtered_timestamps_5 = timestamps[4:]
filtered_timestamps_10 = timestamps[9:]

##std_deviation calculations are false, see README/To note
print("response_time_90_raw:", response_time_90(
    timestamps,
    az_values,
    9.81,
    12.00
), "\n")
print("MA(3)_response_time_90:", response_time_90(
    filtered_timestamps_3,
    filtered_az_3,
    9.81,
    12.00
), "\n")
print("MA(5)_response_time_90:", response_time_90(
    filtered_timestamps_5,
    filtered_az_5,
    9.81,
    12.00
), "\n")
print("MA(10)_response_time_90:", response_time_90(
    filtered_timestamps_10,
    filtered_az_10,
    9.81,
    12.00
), "\n")
##
#with负责打开和使用文件，我们现在已经将数据存入列表timestamp和acceleration了，于是跳出with开始画图
plot_imu_data(
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
)