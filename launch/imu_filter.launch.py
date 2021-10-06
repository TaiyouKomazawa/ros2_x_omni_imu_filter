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
    return LaunchDescription([
        #Node(
        #    package='ros2_x_omni_imu_filter',
        #    executable='odom_refresh_node',
        #),
        Node(
            package='ros2_imu_filter_madgwick',
            executable='imu_filter_node',
            remappings=[('imu/data_raw', 'x_omni/imu'),
                        ('imu/mag', 'x_omni/magnetic_field'),
                        ('imu/date', 'x_omni/imu/filtered')
            ],
            parameters=[
                    {'gain': 0.05},
                    {'zeta': 0.001},
                    {'use_mag': True},
                    {'world_frame': 'nwu'},
                    {'use_magnetic_field_msg': True},
                    {'fixed_frame': "base_link"},
                    {'publish_debug_topics': False},
                    {'remove_gravity_vector':True},
                    #{'stateless': True}
            ],
        )
    ])
