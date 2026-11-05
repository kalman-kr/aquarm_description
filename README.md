# AQUARM Description

Description package for the KALMAN AQUARM manipulator.

## Overview

This repository contains robot descriptions, meshes, RViz configurations for the AQUARM manipulator.
It supports a single arm with gripper and RViz visualization.

## Package Structure

```text
.
├── meshes/                 # AQUARM visual meshes
├── rviz/
│   └── rviz.rviz
├── urdf/                   # URDF and Xacro descriptions
│   ├── aquarm_origin/
│   ├── aquarm_gripper/
│   ├── aquarm_macro.xacro
│   └── aquarm_origin_with_gripper.urdf
├── utils.py                # Path resolution and mesh path rewriting
├── viewer_aquarm.py        # Single-arm RViz viewer
├── viewer_gripper.py       # Gripper-only RViz viewer
├── CMakeLists.txt
└── package.xml
```

## Build

Building is optional for the viewers below, but required for other packages to
resolve `package://aquarm_description/...` and `$(find aquarm_description)`.

Clone the repository into the `src/` directory of a ROS 2 workspace, then from
the workspace root:

```bash
colcon build --packages-select aquarm_description
source install/setup.bash
```

The descriptions are installed to `share/aquarm_description/`, and the viewers
become available through `ros2 run`.

To pull in the runtime dependencies listed in `package.xml` first, run
`rosdep install --from-paths src --ignore-src -r -y` (needs `rosdep init` and
`rosdep update` once per machine).

## Visualization

After a build, run a viewer from anywhere:

```bash
ros2 run aquarm_description viewer_aquarm.py
ros2 run aquarm_description viewer_gripper.py
```

Without a build, run them directly from the repository root:

```bash
python3 viewer_aquarm.py
python3 viewer_gripper.py
```

`viewer_aquarm.py` displays `urdf/aquarm_origin_with_gripper.urdf`.

Both forms behave identically. A checkout takes priority over an installed
copy, so edits to a working tree take effect without rebuilding.

All viewers open `joint_state_publisher_gui` by default. Disable it when another node publishes `/joint_states`:

```bash
ros2 run aquarm_description viewer_aquarm.py --no-joint-gui
```

## License

Copyright 2026 KALMAN Inc.

This package, including its code, documentation, URDF/Xacro descriptions,
STL meshes, and RViz configuration, is licensed under the [Apache License, Version 2.0](LICENSE).
External dependencies retain their own licenses.
