from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from .loader import QuestionsDocxWithLatexLoader


def build_vectorstore(doc_paths: list, embedding) -> FAISS:
    all_docs = []
    for path in doc_paths:
        filename = path.split("/")[-1]
        doc_loader = QuestionsDocxWithLatexLoader(path)
        all_docs.extend(doc_loader.load())
    vectorstore = FAISS.from_documents(all_docs, embedding)
    vectorstore.save_local("data/faiss_index")
    return vectorstore


def load_vectorstore(embedding) -> FAISS:
    return FAISS.load_local("data/faiss_index", embedding)
