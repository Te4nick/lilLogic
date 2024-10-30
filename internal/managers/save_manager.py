from dataclasses import dataclass
import os
from pathlib import Path
import json

from internal.nodeedit import Node, NodeLink, NodeData, NodeLinkData, FieldData
from internal.utils import dpg2class


@dataclass
class SaveData:
    nodes: list[dict]  # NodeData
    links: list[dict]  # NodeLinkData


class SaveMan:
    @classmethod
    def _validate_save(cls, data: dict) -> None:
        save_data = SaveData(**data)
        for node in save_data.nodes:
            node_data = NodeData(**node)
            for field in node_data.fields.values():
                FieldData(**field)

        for link in save_data.links:
            NodeLinkData(**link)

    @classmethod
    def get_default_save_path(cls) -> Path:
        save_dir = Path.home()
        if Path.exists(save_dir / "Documents"):
            save_dir = save_dir / "Documents"
        else:
            save_dir = save_dir / "documents"

        return save_dir / "lilLogic"

    @classmethod
    def write_save(cls, name: str, data: dict) -> None:
        cls._validate_save(data)
        save_dir = cls.get_default_save_path()
        os.makedirs(save_dir, exist_ok=True)

        with open(save_dir / f"{name}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @classmethod
    def read_save(cls, path: str) -> dict:
        data: dict
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        cls._validate_save(data)
        return data
