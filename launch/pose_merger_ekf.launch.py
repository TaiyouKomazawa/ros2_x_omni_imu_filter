import os

from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import TextSubstitution
from launch_ros.actions import Node
from launch_ros.actions import PushRosNamespace


def generate_launch_description():

    imu_filter_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory(
                'ros2_x_omni_imu_filter'), 'imu_filter.launch.py')
        )
    )
    return LaunchDescription([
        imu_filter_launch,
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',

            output='screen',
            parameters=[os.path.join(get_package_share_directory(
                "ros2_x_omni_imu_filter"), 'params', 'ekf.yaml')
            ],
        ),
    ])
