import abc
import base64
import uuid
from typing import List

import crawler.object_store
from crawler.model import FilePackage, Session, File


class FilePackageBase(abc.ABC):
    @abc.abstractmethod
    def get_package_id(self) -> str:
        pass

    @abc.abstractmethod
    def add_file(self, blob: bytes, source_url: str):
        pass


class ScreenshotPackage(FilePackageBase):
    def __init__(self, start_url: str | None, package_id: int = None):
        self.object_store = crawler.object_store.FileSystemObjectStore()
        if package_id is None:
            package_orm = FilePackage(start_url=start_url)
            with Session() as db_sess:
                db_sess.add(package_orm)
                db_sess.commit()
                self.package_id = package_orm.id
        else:
            self.package_id = package_id

    def add_file(self, blob: bytes, source_url: str):
        with Session() as db_sess:
            file_orm = File(source_url=source_url, package_id=self.package_id)
            file_uri = self.object_store.save(blob=blob, name=self._generate_filename())
            file_orm.file_uri = file_uri
            db_sess.add(file_orm)
            db_sess.commit()

    def get_package_id(self) -> int:
        return self.package_id

    def get_files(self) -> List[dict]:
        with Session() as db_sess:
            files = db_sess.query(File).filter(File.package_id == self.package_id)
            return [{"file_id": file.id, "source_url": file.source_url, "file_uri": file.file_uri}
                    for file in files]

    def get_file_path(self, file_id: int) -> bytes:
        with Session() as db_sess:
            file = db_sess.query(File).filter(File.package_id == self.package_id, File.id == file_id).one()
            return file.file_uri

    @classmethod
    def from_id(cls, package_id: int):
        return cls(None, package_id)

    def _generate_filename(self):
        return f"{self.package_id}_{uuid.uuid4().hex}.png"
