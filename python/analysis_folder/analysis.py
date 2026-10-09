import math

def calculate_std_deviation(data):#计算标准差
    mean = sum(data) / len(data)

    squared_errors = []
    for value in data:
        squared_errors.append((value - mean)**2)
    variance = sum(squared_errors) / len(data)

    return math.sqrt(variance)# return type: int;返回标准差

def response_time_90(#90%响应时间
    timestamps,
    filtered_data,
    initial_value,
    final_value
):
    threshold = initial_value + 0.9 * (final_value - initial_value)

    for timestamp, value in zip(timestamps, filtered_data):#zip:将两个列表一对一配对成(x, y)形式
        if value >= threshold:#filtered数据达到90%
            return timestamp

    return None