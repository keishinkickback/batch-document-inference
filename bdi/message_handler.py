from typing import List

from .data import Document, Sentence
from .message_io import MessageIO, SampleIO
from .tokenizer import SentenceTokenizer, SyntokSentenceTokenizer


class MessageHandler:
    """Handle a batch of messages to process sentence batch

    Args:
        meaageio: MessageIO instance
        sentence_tokenizer: SentenceTokenizer instance
    """

    def __init__(
            self,
            messageio: MessageIO = SampleIO(),
            sentence_tokenizer: SentenceTokenizer = SyntokSentenceTokenizer()
    ) -> None:
        self.messageio = messageio
        self.sentence_tokenizer = sentence_tokenizer
        self.messages: List[dict] = []
        self.documents: List[Document] = []

    def append_messages(self, messages: List[dict], keep_old=False) -> None:
        """Accumulate messages

        Args:
            messages: a list of messages (dict)
            keep_old: if enabled, keep old messages and add new messages to the collection

        Returns:
            None
        """
        if keep_old:
            if 0 < len(self.documents):
                raise RuntimeError('messages have already converted to documents. Set keep_old=False')
        else:
            self.messages = []
            self.documents = []
        self.messages += messages

    def _message2document(self) -> None:
        """Creates message objects from messages

        Returns:
            None
        """
        for index, message in enumerate(self.messages):
            title, body = self.messageio.extract_text(message)
            doc = Document(id=index, title=title, body=body)
            self.documents.append(doc)

    def to_documents(self) -> List[Document]:
        """
        Returns:
            A list of documents
        """
        self._message2document()
        return list(self.documents)

    def update_documents(self, documents: List[Document]) -> None:
        """Delete old messages and assign new messages
        Args:
            documents:

        Returns:
            None
        """
        self.documents = documents

    def to_sentences(self, use_title=True) -> List[Sentence]:
        """Extract sentences from messages and return a list of Sentences
        Returns:
            a list of Sentences
        """

        # convert messages to documents
        if not self.documents:
            self._message2document()

        lst_sentences = []
        for document in self.documents:

            if use_title:
                for index, str_sent in enumerate(self.sentence_tokenizer.sentence_tokenize(document.title)):
                    lst_sentences.append(
                        Sentence(id_document=document.id, text=str_sent, id_sentence=index, title=True))

            for index, str_sent in enumerate(self.sentence_tokenizer.sentence_tokenize(document.body)):
                lst_sentences.append(Sentence(id_document=document.id, text=str_sent, id_sentence=index))

        return lst_sentences

    def add_sentence_results(self, sentences: List[Sentence]):
        """Append sentence results to documents. Use sentence.id_document for aggregation

        Args:
            sentences:

        Returns:

        """
        for sent in sentences:
            self.documents[sent.id_document].result = self.documents[sent.id_document].result + sent.result

    def to_document_results(self) -> List[dict]:
        """Append results and return messages
        Returns:
            A list of messages that appended their results
        """
        assert len(self.messages) == len(self.documents)
        results = []
        for document in self.documents:
            message = self.messageio.append_result(self.messages[document.id], document.result.to_dict())
            results.append(message)
        return results
