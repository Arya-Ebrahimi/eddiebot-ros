from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import OpaqueFunction, DeclareLaunchArgument
from launch.substitutions import Command, PathJoinSubstitution
from launch.substitutions.launch_configuration import LaunchConfiguration
from launch_ros.descriptions import ParameterValue
from launch_ros.actions import Node


ARGUMENTS = [
    DeclareLaunchArgument('model', default_value='eddie_kinect_v1',
                          choices=['eddie_kinect_v1', 'eddie_kinect_v2'],
                          description='Eddiebot Model'),
    DeclareLaunchArgument('use_sim_time', default_value='false',
                          choices=['true', 'false'],
                          description='use_sim_time'),
    DeclareLaunchArgument('robot_name', default_value='eddiebot',
                          description='Robot name'),
    DeclareLaunchArgument('namespace', default_value=LaunchConfiguration('robot_name'),
                          description='Robot namespace'),
]


def generate_launch_description():
    return LaunchDescription(ARGUMENTS + [
        OpaqueFunction(function=launch_setup)
    ])


def launch_setup(context, *args, **kwargs):
    pkg_eddiebot_description = get_package_share_directory('eddiebot_description')
    xacro_file = PathJoinSubstitution([pkg_eddiebot_description,
                                       'robots',
                                       LaunchConfiguration('model'),
                                       'eddiebot.urdf.xacro'])
    namespace = LaunchConfiguration('namespace')

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
            {'robot_description': ParameterValue(Command([
                'xacro', ' ', xacro_file, ' ',
                'gazebo:=ignition', ' ',
                'namespace:=', namespace]), value_type=str)},
        ],
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static')
        ]
    )

    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static')
        ]
    )

    # Add nodes to LaunchDescription
    return [
            robot_state_publisher,
            joint_state_publisher
    ]
