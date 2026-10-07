def complementary_filter(
    previous_angle,
    angular_velocity,
    dt,
    accelerometer_angle,
    alpha=0.98#gyro权重
):
    gyro_angle = previous_angle + angular_velocity * dt#一次积分

    angle = (
        alpha * gyro_angle
        + (1 - alpha) * accelerometer_angle
    )#一次加权纠偏

    return angle

