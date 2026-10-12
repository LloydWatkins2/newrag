import os
import pandas as pd
from abc import abstractmethod, ABC
from pathlib import Path
from pandas.errors import ParserError

from pandas.errors import ParserError,EmptyDataError


class DocumentError(Exception):
    """Base exception cho document pipeline."""

    pass


class DocumentValidationError(DocumentError):
    """Base exception cho validation."""

    pass


class DocumentNotFoundError(DocumentValidationError):
    """File không tồn tại."""

    pass


class EmptyDocumentError(DocumentValidationError):
    """File tồn tại nhưng rỗng."""

    pass


class DocumentParsingError(DocumentError):
    """Không thể parse document."""

    pass


class WrongFileType(DocumentValidationError):
    """Wrong end file extensions"""

    pass


class passers(ABC):
    @property
    @abstractmethod
    def supported_extension(self) -> str:
        pass

    @abstractmethod
    def parser(self, destination) -> str:
        """passer methods"""
        pass


class txtpasser(passers):
    @property
    def supported_extension(self) -> str:
        return ".txt"

    def parser(self, destination) -> str:
        with open(destination, "r", encoding="UTF8") as f:
            ans = f.read()
        return ans


class csvpasser(passers):
    @property
    def supported_extension(self):
        return ".csv"

    def parser(self, destination) -> str:
        try:
            doc = pd.read_csv(destination, encoding="UTF8")
            return doc.to_string()
        except ParserError as e:
            raise DocumentParsingError(
                f"cant analyze csv file{e}"
            ) from e
        except EmptyDataError as e:
            raise DocumentParsingError(
                f"data in table is invalid: errors {e}"
            ) from e


class Document:
    def __init__(self, content: str, metadata: dict) -> None:
        self.content = content
        self.metadata = metadata


class DocumentLoader(ABC):
    def __init__(self, destination: str, parser: passers):
        self.destination = destination
        self.parser = parser

    def validate(self) -> None:
        root = Path(self.destination).suffix
        try:
            size = os.path.getsize(self.destination)

        except FileNotFoundError as e:
            raise DocumentNotFoundError(
                f"Document not found: {self.destination}"
            ) from e

        if size == 0:
            raise EmptyDocumentError(f"Document is empty: {self.destination}")
        if self.parser.supported_extension != root:
            raise WrongFileType(f"extensions not appropriate:{self.destination}")

    def metaextraction(self) -> dict:
        meta = Path(self.destination)

        return {
            "name": meta.name,
            "type": meta.suffix,
            "stats": meta.stat(),
        }

    def load(self) -> Document:
        """
        Orchestrate toàn bộ quá trình:

        validate -> parse -> metadata -> Document
        """
        self.validate()

        content = self.parser.parser(self.destination)
        metadata = self.metaextraction()

        return Document(content=content, metadata=metadata)


if __name__ == "__main__":
    file1 = "doc.txt"
    file2 = "doc.csv"
    f1 = DocumentLoader(file1, txtpasser()).load()
    print(f1.content)
    f2 = DocumentLoader(file2, csvpasser()).load()
    print(f2.content)
    f3 = DocumentLoader(file2, txtpasser()).load()
    print(f3.content)
