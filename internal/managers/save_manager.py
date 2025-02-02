import os
from pathlib import Path

from internal.nodeedit import NodeData, NodeLinkData, FieldData
from pydantic import BaseModel


class SaveData(BaseModel):
    nodes: list[NodeData]
    links: list[NodeLinkData]


class SaveMan:

    @classmethod
    def default_dir(cls) -> Path:
        save_dir = Path.home()
        if Path.exists(save_dir / "Documents"):
            save_dir = save_dir / "Documents"
        else:
            save_dir = save_dir / "documents"

        os.makedirs(save_dir, exist_ok=True)
        return save_dir / "lilLogic"

    @classmethod
    def write_save(cls, filepath: str, save_data: SaveData) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(save_data.model_dump_json(indent=4))

    @classmethod
    def read_save(cls, filepath: str) -> SaveData:
        save_data: SaveData
        with open(filepath, "r", encoding="utf-8") as f:
            save_data = SaveData.model_validate_json(f.read())

        return save_data
