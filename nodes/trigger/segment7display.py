from internal.nodeedit import Node
from internal.nodeedit.fields import Field, BoolField
import dearpygui.dearpygui as dpg
from typing import Any

from loguru import logger
import sys

logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
)


class Segment7Display(Node):
    node_type = "7-Segment Display"

    def build(self):
        for pin in ["A", "B", "C", "D", "E", "F", "G", "DP"]:
            self.add_field(
                BoolField(
                    pin,
                    parent=self.alias,
                    callback=self.calculate,
                    attribute_type=0,
                ),
            )

        self.add_field(ColorField("COLOR", parent=self.alias))

    def calculate(self):
        res = 0
        shift = 7
        for pin in ["A", "B", "C", "D", "E", "F", "G", "DP"]:
            res += self.get_field_value(pin) << shift
            shift -= 1
        self.set_field_value("COLOR", res)


class ColorField(Field):

    def __init__(
        self,
        label: str,
        parent: int | str = None,
        callback: Any | None = None,
        readonly: bool = False,
        user_data: dict[str, Any] = None,
        default_value: int = False,
    ):
        super().__init__(
            label=label,
            parent=parent,
            attribute_type=2,
            callback=callback,
            default_value=default_value,
        )

        self.label = label
        self.parent = parent
        self.readonly = readonly
        self.value = default_value

        self.__segments: list[DisplaySegment] = []

        self.dpg_field: int | str = ""
        self.dpg_group: int | str = ""
        self.dpg_plot: int | str = ""

        self.color_red = (255, 0, 0, 255)  # RGBA RED
        self.color_black = (0, 0, 0, 255)  # RGBA BLACK

    def __del__(self):
        super().__del__()
        dpg.delete_item(self.dpg_field)
        dpg.delete_item(self.dpg_attr)

    def _on_value_changed(self):
        tmp_val = self.value
        for i in range(8):
            if tmp_val & 0b1:
                self.__segments[-1 - i].on()
            else:
                self.__segments[-1 - i].off()
            tmp_val >>= 1

    def __on_dpg_callback(self):
        def value_changed(
            sender: Any = None,
            app_data: Any = None,
            user_data: Any = None,
        ):
            # ic(self.parent + f"_{self.label}",
            #    self.__links_to)
            logger.debug(
                f"{self.tag}: __on_dpg_callback: value: {dpg.get_value(sender)}"
            )
            self.receive_value(dpg.get_value(sender))

        return value_changed

    def build(self, user_data: dict[str, Any] = None):
        if user_data is None:
            user_data = {}
        user_data["class"] = self
        self.dpg_group = dpg.add_group(parent=self.dpg_attr)
        self.dpg_plot = dpg.add_plot(
            parent=self.dpg_group,
            no_menus=False,
            no_title=True,
            no_box_select=True,
            no_mouse_pos=True,
            width=2 * 70,
            height=2 * 90,
            equal_aspects=True,
            tag=self.dpg_attr + "PLOT",
        )
        default_x = dpg.add_plot_axis(
            axis=0,
            no_gridlines=False,
            no_tick_marks=True,
            no_tick_labels=True,
            lock_min=True,
            parent=self.dpg_plot,
        )
        default_y = dpg.add_plot_axis(
            axis=1,
            no_gridlines=False,
            no_tick_marks=True,
            no_tick_labels=True,
            lock_min=True,
            parent=self.dpg_plot,
        )

        dpg.set_axis_limits(axis=default_x, ymin=0, ymax=7)
        dpg.set_axis_limits(axis=default_y, ymin=0, ymax=9)

        dpg.add_inf_line_series(x=[n for n in range(7)], parent=default_x)
        dpg.add_inf_line_series(
            x=[n for n in range(9)], parent=default_y, horizontal=True
        )

        # dpg.draw_text(pos=[0.5, 11], text="GAME OVER", size=1, parent=self.dpg_plot)  # TEXT

        self.__segments.append(
            DisplaySegment(
                pmin=[2.5, 8.5],
                pmax=[4.5, 8.5],
                parent=self.dpg_plot,  # SEGMENT_A
            )
        )

        self.__segments.append(
            DisplaySegment(
                pmin=[5.5, 7.5],
                pmax=[5.5, 5.5],
                parent=self.dpg_plot,  # SEGMENT_B
            )
        )

        self.__segments.append(
            DisplaySegment(
                pmin=[5.5, 3.5],
                pmax=[5.5, 1.5],
                parent=self.dpg_plot,  # SEGMENT_C
            )
        )

        self.__segments.append(
            DisplaySegment(
                pmin=[2.5, 0.5],
                pmax=[4.5, 0.5],
                parent=self.dpg_plot,  # SEGMENT_D
            )
        )

        self.__segments.append(
            DisplaySegment(
                pmin=[1.5, 3.5],
                pmax=[1.5, 1.5],
                parent=self.dpg_plot,  # SEGMENT_E
            )
        )

        self.__segments.append(
            DisplaySegment(
                pmin=[1.5, 7.5],
                pmax=[1.5, 5.5],
                parent=self.dpg_plot,  # SEGMENT_F
            )
        )

        self.__segments.append(
            DisplaySegment(
                pmin=[2.5, 4.5],
                pmax=[4.5, 4.5],
                parent=self.dpg_plot,  # SEGMENT_G
            )
        )

        self.__segments.append(
            DisplaySegment(
                pmin=[6.5, 0.5],
                pmax=[6.5, 0.5],
                parent=self.dpg_plot,  # SEGMENT_DP
            )
        )


class DisplaySegment:
    COLOR_RED = (255, 0, 0, 255)  # RGBA RED
    COLOR_BLACK = (0, 0, 0, 255)  # RGBA BLACK

    def __init__(
        self,
        pmin: list[float] | tuple[float, ...],
        pmax: list[float] | tuple[float, ...],
        parent: int | str = None,
        default_value: bool = False,
    ):
        self.pmin = pmin
        self.pmax = pmax
        self.parent = parent

        self.dpg_rect: int | str = dpg.draw_rectangle(
            pmin=self.pmin,
            pmax=self.pmax,
            color=self.COLOR_RED if default_value else self.COLOR_BLACK,
            parent=self.parent,
        )

    def on(self):
        dpg.delete_item(self.dpg_rect)
        self.dpg_rect = dpg.draw_rectangle(
            pmin=self.pmin,
            pmax=self.pmax,
            color=self.COLOR_RED,
            parent=self.parent,
        )

    def off(self):
        dpg.delete_item(self.dpg_rect)
        self.dpg_rect = dpg.draw_rectangle(
            pmin=self.pmin,
            pmax=self.pmax,
            color=self.COLOR_BLACK,
            parent=self.parent,
        )
