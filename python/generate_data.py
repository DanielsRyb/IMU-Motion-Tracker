import csv#导入 csv模块

sample_rate = 100#定义变量采样率，单位为Hz
duration = 10#持续时间

dt = 1 / sample_rate#采样点时间间隔

for i in range(sample_rate * duration):#for循环，次数为(sample_rate * duration)，从0开始
    timestamp = i * dt
    print(f"{timestamp:.2f}")
