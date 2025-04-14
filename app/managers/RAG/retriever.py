from langchain.prompts import PromptTemplate


def retrieve_examples(question: str, vectorstore, k=3):
    results = vectorstore.similarity_search(question, k=k)
    example_str = "\\n".join([
        f"[{doc.metadata['source_file']} #{doc.metadata['index']}]\\n{doc.page_content}"
        for doc in results
    ])
    return results
