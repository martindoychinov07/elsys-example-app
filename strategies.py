from abc import ABC, abstractmethod

# Strategy interface
class FileProcessingStrategy(ABC):
    @abstractmethod
    def process(self, content: bytes):
        pass

# Concrete strategies
class TextFileStrategy(FileProcessingStrategy):
    def process(self, content: bytes):
        return content.decode('utf-8').upper()

class BinaryFileStrategy(FileProcessingStrategy):
    def process(self, content: bytes):
        return content[::-1]  # just reverse bytes for demo

# Context
class FileProcessor:
    def __init__(self, strategy: FileProcessingStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: FileProcessingStrategy):
        self.strategy = strategy

    def execute(self, content: bytes):
        return self.strategy.process(content)

# Usage example
if __name__ == "__main__":
    processor = FileProcessor(TextFileStrategy())
    print(processor.execute(b"Hello World"))

    processor.set_strategy(BinaryFileStrategy())
    print(processor.execute(b"Hello World"))
