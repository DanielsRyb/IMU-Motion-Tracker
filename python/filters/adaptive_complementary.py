def calculate_acceleration_magnitude(ax, ay, az):
    return (ax**2 + ay**2 + az**2) ** 0.5#对加速度取模

def calculate_alpha(
    acceleration_magnitude,
    alpha_normal=0.98,
    alpha_dynamic=0.995,#动态时加速度不能作为主要参照，减小权重
    threshold=0.025#阈值
):
    acceleration_error = abs(acceleration_magnitude - 9.81)#abs：绝对值函数
    relative_error = acceleration_error/9.81#相对误差，%
    if relative_error < threshold:
        return alpha_normal

    return alpha_dynamic


def adaptive_complementary_filter(
    previous_angle,
    angular_velocity,
    dt,
    accelerometer_angle,
    alpha#要作为参数从calculate_alpha传入
):
    gyro_angle = previous_angle + angular_velocity * dt

    angle = (
        alpha * gyro_angle
        + (1 - alpha) * accelerometer_angle
    )

    return angle





