import os
import pandas as pd
from abc import abstractmethod, ABC
from pathlib import Path

from pandas.errors import EmptyDataError, ParserError

class Document:
    def __init__(self,content:str,metadata:dict) -> None:
        self.content=content
        self.metadata=metadata
    @classmethod
    def from_csv(cls,df:pd.DataFrame,metadata:dict) -> 'Document':
        # sử lý df thành str.
        return cls(content=df,metadata=metadata)

class contexmng:
    def __init__(self,destination,mode) -> None:
        self.destination=destination
        self.mode=mode
    def __enter__(self):
        self.file=open(self.destination,mode=self.mode,encoding="UTF-8")
        return self.file
    def __exit__(self,exc_type,exc_val,traceback):
        if exc_type is not None:
            print(f'error dectacted {exc_type.__name__};code error {exc_val}')
            self.file.close()
            return False;
        else:
            print("done")
            self.file.close()
            return True


class DocumentLoader(ABC):
    @staticmethod
    def validate(destination):
        try:
            if(os.path.getsize(destination)>0): 
                print("Path validated to open")
            else:
                print("File empty")
                raise EmptyDataError
        except FileNotFoundError as e:
            print(f"No file found in this self.destination, debug messages: {e}")
            raise FileNotFoundError
       
    @abstractmethod
    def loader() -> Document:
        pass

class txtloader(DocumentLoader):
    def __init__(self,destination) -> None:
        self.destination=destination
    def loader(self):
        DocumentLoader.validate(self.destination)
        with contexmng(self.destination,"r+")as f:
            content=f.read();
        meta=Path(self.destination)
        metadata={
            "name":meta.name,
            "type":meta.suffix,
            "stats":meta.stat(),
        }
        return Document(content,metadata);
class csvloader(DocumentLoader):
    def __init__(self,destination) -> None:
        self.destination=destination
 
    def loader(self):
        try:
            f=pd.read_csv(self.destination,encoding="UTF-8")   
            meta=Path(self.destination)
            metadata={
                "name":meta.name,
                "type":meta.suffix,
                "stats":meta.stat(),
            }
            return Document.from_csv(f,metadata)
        except ParserError as e:
            print(f"parser error {e} occurred, No file openned")

Doc=txtloader("text.txt").loader()
