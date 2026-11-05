#!/usr/bin/env python3
import argparse
import subprocess
import tempfile
from pathlib import Path

import rclpy
from rclpy.node import Node

from utils import (
    PACKAGE_NAME,
    resolve_package_dir,
    rewrite_mesh_paths_to_local_files,
)


class DisplayNode(Node):
    def __init__(self, urdf_name: str, launch_joint_gui: bool = True):
        super().__init__('display_urdf')
        self.temp_urdf_path = None

        package_dir = resolve_package_dir(__file__)
        urdf_path = package_dir / 'urdf' / urdf_name
        config_path = package_dir / 'rviz' / 'rviz.rviz'

        urdf = urdf_path.read_text(encoding='utf-8')
        urdf = rewrite_mesh_paths_to_local_files(
            urdf,
            package_name=PACKAGE_NAME,
            package_dir=package_dir,
            base_dir=urdf_path.parent,
        )

        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.urdf', delete=False, encoding='utf-8'
        ) as f:
            f.write(urdf)
            self.temp_urdf_path = f.name

        subprocess.Popen([
            'ros2',
            'run',
            'robot_state_publisher',
            'robot_state_publisher',
            self.temp_urdf_path,
        ])

        if launch_joint_gui:
            subprocess.Popen([
                'ros2',
                'run',
                'joint_state_publisher_gui',
                'joint_state_publisher_gui',
            ])

        subprocess.Popen(['ros2', 'run', 'rviz2', 'rviz2', '-d', str(config_path)])

    def destroy_node(self):
        if self.temp_urdf_path:
            Path(self.temp_urdf_path).unlink(missing_ok=True)
        super().destroy_node()


def main(args=None, urdf_name='aquarm_origin_with_gripper.urdf'):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--no-joint-gui',
        action='store_true',
        help='Do not launch joint_state_publisher_gui; use external /joint_states instead.',
    )
    parsed_args = parser.parse_args(args=args)

    rclpy.init(args=args)
    node = DisplayNode(
        urdf_name,
        launch_joint_gui=not parsed_args.no_joint_gui,
    )
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
