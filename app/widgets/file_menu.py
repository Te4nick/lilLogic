import dearpygui.dearpygui as dpg
from internal.managers import SaveMan
from internal.utils import dpg2class


class FileMenu:
    def __init__(self, parent: int | str = None):
        self.__file_path_name: str = ""
        self.__save_dir: str = SaveMan.default_dir()
        self.__node_editor = dpg2class("NodeEditor")
        self.__node_selector = dpg2class("NodeSelector")

        with dpg.menu(label="File", parent=parent):
            dpg.add_menu_item(label="New", callback=self.__on_file_new)
            dpg.add_menu_item(label="Save", callback=self.__on_file_save)
            dpg.add_menu_item(label="Save As", callback=self.__on_file_save_as)
            dpg.add_menu_item(label="Open", callback=self.__on_file_open)

    def __build_file_dialog(self, callback):
        with dpg.file_dialog(
            label="Save Canvas Changes",
            modal=True,
            directory_selector=False,
            default_path=self.__save_dir,
            default_filename="lilLogic",
            width=600,
            height=400,
            callback=callback,
        ):
            dpg.add_file_extension(".json", color=(0, 255, 0, 255))

    def __on_file_new(self):
        self.__on_file_save()
        self.__node_editor.clear_canvas()
        self.__file_path_name = ""

    def __on_file_save(self):
        if self.__file_path_name:
            SaveMan.write_save(
                self.__file_path_name, self.__node_editor.get_nodes_data()
            )
            return

        self.__on_file_save_as()

    def __on_file_save_as(self):
        def save_as(_, app_data):
            print(app_data)
            self.__file_path_name = app_data["file_path_name"]
            self.__save_dir = app_data["current_path"]
            SaveMan.write_save(
                self.__file_path_name, self.__node_editor.get_nodes_data()
            )

        self.__build_file_dialog(save_as)

    def __on_file_open(self):
        def import_save(_, app_data):
            save_data = SaveMan.read_save(app_data["file_path_name"])
            self.__node_editor.clear_canvas()
            self.__node_selector.add_from_data(save_data.nodes)
            self.__node_editor.create_links(save_data.links)

        self.__build_file_dialog(import_save)
