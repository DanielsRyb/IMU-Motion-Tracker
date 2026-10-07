def moving_average(data: list[float], window_size: int) -> list[float]:#type hint类型提示，起到一个提醒的作用，并不能防止错误类型输入

    #添加window_size的限制条件
    if window_size <= 0:
        raise ValueError("window_size must be positive")

    if window_size > len(data):
        raise ValueError("window_size cannot be larger than data length")


    filtered_data = []

    for i in range(window_size - 1, len(data)):
        window = data[i - (window_size - 1):i + 1]#window取window_size个值，并且对齐第一个从data[0]开始的window
        average = sum(window) / window_size#取这window_size个值的平均
        filtered_data.append(average)

    return filtered_data