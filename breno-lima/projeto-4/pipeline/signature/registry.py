import json
import os

_DEFAULT_REGISTRY_PATH = "processed_hashes.json"


class _Registry:
    def __init__(self, registry_path: str = _DEFAULT_REGISTRY_PATH):
        self.registry_path = registry_path
        self.registry = self.load_registry()

    def load_registry(self) -> dict:
        if not os.path.exists(self.registry_path):
            return {}
        with open(self.registry_path, "r") as f:
            return json.load(f)

    def save_registry(self) -> None:
        with open(self.registry_path, "w") as f:
            json.dump(self.registry, f, indent=2)

    def is_already_processed(self, file_hash: str) -> bool:
        return file_hash in self.registry

    def mark_as_processed(self, file_hash: str, metadata: dict) -> None:
        self.registry[file_hash] = metadata


registry = _Registry()
