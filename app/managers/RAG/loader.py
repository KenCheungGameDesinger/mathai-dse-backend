import logging

from langchain.document_loaders.base import BaseLoader
from langchain.schema import Document as LCDocument
import re
from docxlatex import Document as DocxLatexDoc


class QuestionsDocxWithLatexLoader(BaseLoader):
    def __init__(self, file_path: str):
        self.file_path = file_path

    # def extract_plain_text(self):
    #     doc = DocxLatexDoc(self.file_path)
    #     return doc.get_text()  # Extracts plain text from the document

    # split_docx_by_question("/content/Law of index_example_1-20 variation.docx", "Law of index_example.docx")
    def _split_docx_by_question(self, doc_path: str, source_file: str):
        doc = DocxLatexDoc(doc_path)
        # full_text = "\n".join([p.text for p in doc.])
        full_text = doc.get_text()
        pattern = r"(?=(?:^|\n)(?:\d+\.\s|[A-Z][^\n]{0,30}\.\n|\t|•))"
        chunks = re.split(pattern, full_text)
        chunk_dicts = []

        for idx, chunk in enumerate(chunks):
            content = chunk.strip()
            if not content or content == '\n' or len(content) < 20:
                continue  # 略過太短的段落
            chunk_dicts.append(LCDocument(page_content=content, metadata={"source_file": source_file, "index": idx}))

        for idx, chunk in enumerate(chunk_dicts):
            chunk.metadata["index"] = idx + 1
        return chunk_dicts

    def load(self):
        doc = self._split_docx_by_question(self.file_path, self.file_path.split("/")[-1])
        print("loaded docs:",doc)
        return doc
