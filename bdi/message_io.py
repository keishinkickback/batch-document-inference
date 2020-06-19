import abc
from typing import Tuple


class MessageIO(metaclass=abc.ABCMeta):
    """Define how to extract text from a message and to append result to a message.
    """

    @abc.abstractmethod
    def extract_text(self, message) -> Tuple[str, str]:
        pass

    @abc.abstractmethod
    def append_result(self, message: dict, result: dict) -> dict:
        pass


class SampleIO(MessageIO):

    def __init__(self):
        pass

    def extract_text(self, message: dict) -> Tuple[str, str]:
        """Extract page_title and body from text_extract's results
        Args:
            message: a message dict contains a text_extract's result
        """
        text_obj = message.get("text_extract", {"page_title": "", "body": ""})
        title = text_obj.get("page_title", "").strip()
        body = text_obj.get("body", "").strip()
        return title, body

    def append_result(self, message: dict, result: dict) -> dict:
        message['ner_result'] = result
        return message


if __name__ == "__main__":
    m = SampleIO()
    m.extract_text({})
