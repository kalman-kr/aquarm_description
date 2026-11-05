cmake_minimum_required(VERSION 3.8)
project(aquarm_description)

find_package(ament_cmake REQUIRED)

# Descriptions, meshes and RViz configs.
#
# The directory layout is preserved verbatim under share/ because the URDFs
# reference meshes relatively.
install(
  DIRECTORY
    meshes
    rviz
    urdf
  DESTINATION share/${PROJECT_NAME}
)

# Viewer entry points, reachable as `ros2 run aquarm_description <script>`.
# utils.py ships beside them because they import it as a sibling module; they
# find the descriptions above through the ament index at runtime.
install(
  PROGRAMS
    viewer_aquarm.py
    viewer_gripper.py
  DESTINATION lib/${PROJECT_NAME}
)

install(
  FILES utils.py
  DESTINATION lib/${PROJECT_NAME}
)

install(
  FILES LICENSE
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
