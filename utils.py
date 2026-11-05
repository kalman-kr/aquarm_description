import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse

PACKAGE_NAME = 'aquarm_description'


def resolve_package_dir(script_file: str | Path, package_name: str = PACKAGE_NAME) -> Path:
    """Locate the directory that holds urdf/, rviz/ and meshes/.

    A checkout containing the script wins over an installed copy, so editing a
    working tree takes effect without rebuilding. When the script runs from
    lib/<package> after a colcon build, the ament index supplies the share
    directory instead.
    """
    checkout = Path(script_file).resolve().parent
    if (checkout / 'urdf').is_dir():
        return checkout

    try:
        from ament_index_python.packages import get_package_share_directory
        share = Path(get_package_share_directory(package_name))
    except Exception as exc:
        raise RuntimeError(
            f'Cannot locate the {package_name} description files. Either run the '
            'script from a checkout, or build the package with colcon and source '
            'the workspace.'
        ) from exc

    if not (share / 'urdf').is_dir():
        raise RuntimeError(f'{share} contains no urdf/ directory; the install is incomplete.')
    return share


def rewrite_mesh_paths_to_local_files(
    urdf_str: str,
    package_name: str,
    package_dir: str | Path,
    base_dir: str | Path | None = None,
) -> str:
    """Resolve mesh paths inside package_dir and verify that every mesh exists."""
    root = ET.fromstring(urdf_str)
    package_dir = Path(package_dir).resolve()
    base_dir = Path(base_dir).resolve() if base_dir is not None else package_dir
    package_prefix = f'package://{package_name}/'

    for mesh in root.findall('.//mesh'):
        filename = mesh.get('filename')
        if not filename:
            continue

        if filename.startswith(package_prefix):
            relative_path = filename.removeprefix(package_prefix)
            mesh_path = package_dir / relative_path
        elif filename.startswith('file://'):
            mesh_path = Path(unquote(urlparse(filename).path))
        elif not urlparse(filename).scheme:
            mesh_path = Path(filename)
            if not mesh_path.is_absolute():
                mesh_path = base_dir / mesh_path
        else:
            raise ValueError(f'Unsupported external mesh URI: {filename}')

        mesh_path = mesh_path.resolve()
        try:
            mesh_path.relative_to(package_dir)
        except ValueError as exc:
            raise ValueError(
                f'Mesh path is outside the package directory: {mesh_path}'
            ) from exc
        if not mesh_path.is_file():
            raise FileNotFoundError(f'Mesh file not found: {mesh_path}')

        mesh.set('filename', mesh_path.as_uri())

    return ET.tostring(root, encoding='unicode', xml_declaration=False)
