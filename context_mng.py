import re


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
            return True;
        else:
            print("done")
            self.file.close()
            return True

with contexmng("word.txt","w") as f:
    f.write("jjenmnv")
    f.read()
print(f.closed)
