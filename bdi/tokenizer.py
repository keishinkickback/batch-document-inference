import abc
from typing import List, Callable

import syntok.segmenter as segmenter


class SentenceTokenizer(metaclass=abc.ABCMeta):
    """Interface of sentence tokenizer"""

    @abc.abstractmethod
    def sentence_tokenize(self, text) -> List[str]:
        pass


class SyntokSentenceTokenizer(SentenceTokenizer):
    """Split a text into sentences using syntok package.

    Args:
        postprocess: post processing function to apply each sentence
    """

    def __init__(self, postprocess: Callable = lambda x: x.replace("\n", " ").replace("\t", " ")):
        self.postprocess = postprocess

    def sentence_tokenize(self, text: str,
                          ) -> List[str]:
        """Split a text into sentences using syntok package

        Args:
            text: text to be split
        """
        lst_sentences = []
        for paragraph in segmenter.analyze(text):
            for sentence in paragraph:
                sentence = "".join(map(str, sentence)).lstrip()
                sentence = self.postprocess(sentence)
                lst_sentences.append(sentence)
        return lst_sentences
