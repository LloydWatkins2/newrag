from abc import ABC,abstractmethod
import pandas as pd
from pandas.io import parsers
class passers(ABC):
    @abstractmethod
    def parser(self,destination)->str:
        """passer methods"""
        pass
class txtpasser(passers):
    def parser(self,destination) -> str:
        with open(destination,"r",encoding="UTF8") as f:
            ans=f.read();
        return ans;
class csvpasser(passers):
    def parser(self,destination) -> str:
        doc=pd.read_csv(destination,encoding="UTF8");
        return doc.to_string()
        
class DocumentLoader:
    def __init__(self,destination: str,parser:passers):
        self.destination=destination;
        self.parser=parser; 
    def load(self):

