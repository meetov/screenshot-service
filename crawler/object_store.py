import abc
import os
import pathlib

from crawler.config import DATA_DIR


class ObjectStore(abc.ABC):
    @abc.abstractmethod
    def save(self, blob: bytes, name: str):
        """Used to save a file to store."""

    @abc.abstractmethod
    def read(self, path: str) -> bytes:
        """Used to read a file from store."""


class FileSystemObjectStore(ObjectStore):
    _base_dir = pathlib.Path(DATA_DIR)

    def save(self, blob: bytes, name: str):
        file_path = self._base_dir / name
        with file_path.open('wb') as file:
            file.write(blob)

        return file_path.as_posix()

    def read(self, path: str) -> bytes:
        with open(path, 'rb') as file:
            return file.read()
