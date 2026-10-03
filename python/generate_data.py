import csv#导入 csv模块
import random
sample_rate = 100#定义变量采样率，单位为Hz
duration = 10#持续时间

dt = 1 / sample_rate#采样点时间间隔

with open("data/simulated.csv", "w", newline="") as file:#open的对象不存在的时候py会创建;"w" - write，表示准备写入，若文件已经存在，则覆盖
#使用newline=""表示py不进行额外的换行转换，让csv自己处理
    writer = csv.writer(file)#创建一个写csv的工具

    for i in range(sample_rate * duration):#for循环，次数为(sample_rate * duration)，从0开始
        timestamp = i * dt
        print(f"{timestamp:.2f}")

        writer.writerow(["timestamp", "ax", "ay", "az", "wx", "wy", "wz"])

        ax = 0.1
        ay = 0.05
        az = 9.81 + random.gauss(0, 0.05)

        wx = 0.01
        wy = -0.02
        wz = 0.03

        writer.writerow([
            f"{timestamp:.2f}",
            f"{ax:.2f}",
            f"{ay:.2f}",
            f"{az:.2f}",
            f"{wx:.2f}",
            f"{wy:.2f}",
            f"{wz:.2f}"
        ])