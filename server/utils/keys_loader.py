import inspect
import json
import logging
import os

from config import Config

logger = logging.getLogger(__name__)


class KeysLoader:
    """Class specifically used for keys management."""

    def __init__(self, config_file: str):
        with open(config_file, "r") as file:
            self.config = json.load(file)
        self.funcs = {name[1:]: inst for name, inst in inspect.getmembers(self)}

    @classmethod
    def get_keys_loader(cls):
        """Get keys loader context."""
        return cls(Config.KEYS_CONFIG_FILE)

    def load_aes_keys(self):
        """Load AES Shamir key parts."""
        key_parts = []
        for conf in self.config["AES_KEYS"]:
            try:
                key_parts.extend(self.funcs[conf["method"]](**conf["params"]))
            except Exception as e:
                logger.warning(f"Key was not loaded with error: {str(e)}")
        return key_parts

    @staticmethod
    def _load_from_files(file_paths):
        """Load keys from files."""
        key_parts = []
        for file_path in file_paths:
            with open(file_path, "r") as file:
                idx, key_share = file.read().split("\n")
                key_parts.append((int(idx), key_share))
        return key_parts