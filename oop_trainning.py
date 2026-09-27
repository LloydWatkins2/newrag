import os
import pandas as pd
from abc import abstractmethod, ABC
from pathlib import Path

from pandas.errors import ParserError


# =========================
# Exceptions
# =========================

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


# =========================
# Document
# =========================

class Document:
    def __init__(self, content: str, metadata: dict) -> None:
        self.content = content
        self.metadata = metadata


# =========================
# Context manager
# =========================

class ContextMNG:
    def __init__(self, destination, mode) -> None:
        self.destination = destination
        self.mode = mode

    def __enter__(self):
        self.file = open(
            self.destination,
            mode=self.mode,
            encoding="UTF-8"
        )
        return self.file

    def __exit__(self, exc_type, exc_val, traceback):
        self.file.close()

        # False/None -> exception tiếp tục propagate
        return False


# =========================
# Base Loader
# =========================

class DocumentLoader(ABC):

    def __init__(self, destination) -> None:
        self.destination = destination

    def validate(self) -> None:
        try:
            size = os.path.getsize(self.destination)

        except FileNotFoundError as e:
            raise DocumentNotFoundError(
                f"Document not found: {self.destination}"
            ) from e

        if size == 0:
            raise EmptyDocumentError(
                f"Document is empty: {self.destination}"
            )

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

        content = self.parse()

        metadata = self.metaextraction()

        return Document(
            content=content,
            metadata=metadata
        )

    @abstractmethod
    def parse(self) -> str:
        pass


# =========================
# TXT Loader
# =========================

class TXTLoader(DocumentLoader):

    def parse(self) -> str:
        with ContextMNG(self.destination, "r") as f:
            return f.read()


# =========================
# CSV Loader
# =========================

class CSVLoader(DocumentLoader):

    def parse(self) -> str:
        try:
            df = pd.read_csv(
                self.destination,
                encoding="UTF-8"
            )

            return df.to_string()

        except ParserError as e:
            raise DocumentParsingError(
                f"Failed to parse CSV: {self.destination}"
            ) from e


# =========================
# Test
# =========================

if __name__ == "__main__":

    try:
        doc = TXTLoader("word.txt").load()

        print(type(doc))
        print(type(doc.content))
        print(doc.metadata)

    except DocumentError as e:
        print(f"Document error: {e}")

    try:
        csv_doc = CSVLoader("asaffe.csv").load()

        print(type(csv_doc))
        print(type(csv_doc.content))
        print(csv_doc.metadata)

    except DocumentError as e:
        print(f"Document error: {e}")
