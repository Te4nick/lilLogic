import os
from pathlib import Path

from internal.nodeedit import NodeData, NodeLinkData, FieldData
from pydantic import BaseModel


class SaveData(BaseModel):
    nodes: list[NodeData]
    links: list[NodeLinkData]


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
    def write_save(cls, name: str, save_data: SaveData) -> None:
        print(save_data)
        save_dir = cls.get_default_save_path()
        os.makedirs(save_dir, exist_ok=True)

        with open(save_dir / f"{name}.json", "w", encoding="utf-8") as f:
            f.write(save_data.model_dump_json(indent=4))

    @classmethod
    def read_save(cls, path: str) -> SaveData:
        save_data: SaveData
        with open(path, "r", encoding="utf-8") as f:
            save_data = SaveData.model_validate_json(f.read())

        return save_data
