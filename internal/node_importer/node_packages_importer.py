import os
import glob

from icecream import ic
import importlib.machinery
from internal.base.base_node import Node


class NodeImporter:
    def __init__(self, path: str | None = None):
        if path is None:
            current_script_path = os.path.abspath(__file__)
            ic(current_script_path)

            # Building the path to the project root directory
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_script_path)))
            ic(project_root)

            # Построение пути к желаемой директории внутри проекта (например, "my_directory")
            self.nodes_dir = os.path.join(project_root, "nodes")
            ic(self.nodes_dir)
        else:
            self.nodes_dir = path

        self.node_dict: dict[str: dict[str: Node]] = {}

        self.__build_node_dict()

    def __build_node_dict(self):
        package_names = self.get_node_packages()
        for name in package_names:
            self.get_package_nodes(name)
        return

    def get_node_packages(self, path: str | None = None) -> list[str]:
        if path is None:
            path = self.nodes_dir

        # Searching for dirs with __init__.py in provided path
        node_packages = glob.glob(os.path.join(path, "*/__init__.py"))

        for package in node_packages:
            package_name = os.path.basename(os.path.dirname(package))
            self.node_dict[package_name] = {}

        return ic(list(self.node_dict.keys()))

    def get_package_nodes(self, package_name: str, path: str | None = None):
        if path is None:
            path = self.nodes_dir

        # Building package __init__.py file path
        init_file_path = os.path.join(path, package_name, "__init__.py")

        ic(package_name, path, init_file_path)

        if os.path.exists(init_file_path):
            pkg_loader = importlib.machinery.SourceFileLoader(package_name, init_file_path)
            ic(pkg_loader.is_package(package_name))

            if pkg_loader.is_package(package_name):

                package = pkg_loader.load_module()

                if hasattr(package, "__all__") and isinstance(package.__all__, list):
                    for node_name in package.__all__:
                        node = getattr(package, node_name, None)
                        if issubclass(node, Node):
                            self.node_dict[package_name][node_name] = node
                ic(package.__all__)

                return package.__all__

    def get_package_names(self) -> list[str]:
        return list(self.node_dict.keys())

    def get_package_node_names(self, package_name: str) -> list[str]:
        return list(self.node_dict[package_name].keys())

    def get_node_class(self, package_name: str, node_name: str) -> Node:
        return self.node_dict[package_name][node_name]


if __name__ == "__main__":
    ic.configureOutput(includeContext=True)
    nimport = NodeImporter()
    npkgs = nimport.get_node_packages()
    for pkg in npkgs:
        ic(pkg, nimport.get_package_nodes(pkg))

    ic(nimport.node_dict)
