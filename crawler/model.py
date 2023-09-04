from typing import List

import sqlalchemy
from sqlalchemy import orm

from crawler.config import SCREENSHOT_DB_CONN_STR


class Base(orm.DeclarativeBase):
    pass


class FilePackage(Base):
    __tablename__ = "file_package"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    start_url: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String)

    files: orm.Mapped[List["File"]] = orm.relationship(
        back_populates="package"
    )


class File(Base):
    __tablename__ = "files"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    source_url: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String)
    file_uri: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String)

    package_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey('file_package.id'))
    package: orm.Mapped["FilePackage"] = orm.relationship(back_populates="files")



engine = sqlalchemy.create_engine(SCREENSHOT_DB_CONN_STR, echo=True)
Base.metadata.create_all(engine)
Session = orm.sessionmaker(engine, expire_on_commit=False)
