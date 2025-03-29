import json

import firebase_admin
from firebase_admin import credentials, firestore
from typing import Any, Dict, List, Optional


# Firestore 通用管理庫
class FirestoreManager:
    def __init__(self, path="service_account_key_generative_exam.json"):
        # 初始化 Firestore
        self.cred = credentials.Certificate(path)
        self.app = firebase_admin.initialize_app(self.cred)
        # print("Firebase initialized successfully!")
        self.db = firestore.client()
        print("Firestore initialized successfully!")

    # def initialize_firebase(service_account_path: str):
    #     """Initialize Firebase using the provided service account path."""
    #     cred = credentials.Certificate(service_account_path)
    #     firebase_admin.initialize_app(cred)
    #     print("Firebase initialized successfully!")

    # 添加單個文檔
    def add_document(self, collection_name: str, document_data: Dict[str, Any], document_id: Optional[str] = None):
        """
        Add a single document to the specified collection.

        :param collection_name: Name of the collection to add the document.
        :param document_data: Data to be added as a document.
        :param document_id: Optional document ID. If None, Firestore will generate a random ID.
        :return: A dictionary with the success message.

        Example usage:
        document_data = {"name": "Alice", "age": 25, "email": "alice@example.com"}
        print(manager.add_document("users", document_data, "user_1"))
        """
        msg = ""
        if document_id:
            self.db.collection(collection_name).document(document_id).set(document_data)
            return {"success": True, "document_id": document_id}
        else:
            print("adding")
            doc_ref = self.db.collection(collection_name).add(document_data)
            return {"success": True, "document_id": doc_ref[1].id, "document_ref": doc_ref[1].get().to_dict()}

    # 批量添加文檔
    def batch_add_documents(self, collection_name: str, documents: List[Dict[str, Any]]):
        """
        Add multiple documents to the specified collection.

        :param collection_name: Name of the collection to add the documents.
        :param documents: A list of dictionaries where each dictionary represents a document's data.
        :return: A dictionary with the success message.

        Example usage:
        batch_data = [{"name": "Bob", "age": 30, "email": "bob@example.com"},
                      {"name": "Charlie", "age": 35, "email": "charlie@example.com"}]
        print(manager.batch_add_documents("users", batch_data))
        """
        batch = self.db.batch()
        for document_data in documents:
            doc_ref = self.db.collection(collection_name).document()
            batch.set(doc_ref, document_data)
        batch.commit()
        return {"success": True, "message": "Batch documents added successfully."}

    # 獲取單個文檔
    def get_document(self, collection_name: str, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single document by ID.

        :param collection_name: Name of the collection containing the document.
        :param document_id: The ID of the document to retrieve.
        :return: Document data as a dictionary if it exists, otherwise None.

        Example usage:
        print(manager.get_document("users", "user_1"))
        """
        doc_ref = self.db.collection(collection_name).document(document_id).get()
        if doc_ref.exists:
            return doc_ref.to_dict()
        return None

    # 獲取集合中的所有文檔
    def get_collection(self, collection_name: str) -> List[Dict[str, Any]]:
        """
        Retrieve all documents in a collection.

        :param collection_name: The name of the collection to retrieve.
        :return: A list of documents, where each document is a dictionary.

        Example usage:
        print(manager.get_collection("users"))
        """
        docs = self.db.collection(collection_name).stream()
        return [doc.to_dict() for doc in docs]

    # 更新單個文檔
    def update_document(self, collection_name: str, document_id: str, update_data: Dict[str, Any]):
        """
        Update a single document by ID.

        :param collection_name: Name of the collection containing the document.
        :param document_id: The ID of the document to update.
        :param update_data: A dictionary of the fields to update and their new values.
        :return: A dictionary with a success message.

        Example usage:
        update_data = {"age": 26}
        print(manager.update_document("users", "user_1", update_data))
        """
        self.db.collection(collection_name).document(document_id).update(update_data)
        return {"success": True, "message": "Document updated successfully."}

    # 批量更新文檔
    def batch_update_documents(self, collection_name: str, updates: Dict[str, Dict[str, Any]]):
        """
        Batch update multiple documents. Updates should be a dictionary where the key is the document ID.

        :param collection_name: Name of the collection containing the documents.
        :param updates: A dictionary where the key is the document ID and the value is the update data.
        :return: A dictionary with the success message.

        Example usage:
        updates = {
            "user_1": {"age": 27},
            "user_2": {"email": "newemail@example.com"}
        }
        print(manager.batch_update_documents("users", updates))
        """
        batch = self.db.batch()
        for document_id, update_data in updates.items():
            doc_ref = self.db.collection(collection_name).document(document_id)
            batch.update(doc_ref, update_data)
        batch.commit()
        return {"success": True, "message": "Batch documents updated successfully."}

    # 刪除單個文檔
    def delete_document(self, collection_name: str, document_id: str):
        """
        Delete a single document by ID.

        :param collection_name: Name of the collection containing the document.
        :param document_id: The ID of the document to delete.
        :return: A dictionary indicating whether the deletion was successful or if the document was not found.

        Example usage:
        result = manager.delete_document("users", "user_1")
        print(result)
        """
        try:
            # 獲取文檔引用
            doc_ref = self.db.collection(collection_name).document(document_id)
            print("deleting")
            # 檢查文檔是否存在
            if doc_ref.get().exists:
                doc_ref.delete()
                return {"success": True, "message": "Document deleted successfully.", "document_id": document_id}
            else:
                return {"success": False, "error": f"Document with ID {document_id} not found."}
        except Exception as e:
            return {"success": False, "error": f"An error occurred: {str(e)}"}

    # 批量刪除文檔
    def batch_delete_documents(self, collection_name: str, document_ids: List[str]):
        """
        Batch delete multiple documents by their IDs.

        :param collection_name: Name of the collection containing the documents.
        :param document_ids: A list of document IDs to delete.
        :return: A dictionary with the success message.

        Example usage:
        document_ids = ["user_1", "user_2"]
        print(manager.batch_delete_documents("users", document_ids))
        """
        batch = self.db.batch()
        for document_id in document_ids:
            doc_ref = self.db.collection(collection_name).document(document_id)
            batch.delete(doc_ref)
        batch.commit()
        return {"success": True, "message": "Batch documents deleted successfully."}


# db_instance = FirestoreManager("service_account_key_generative_exam.json")
db_instance = FirestoreManager(path="service_account_key_metamersive.json")

# 示例代碼
# if __name__ == "__main__":
#     # 初始化 Firebase
#     service_account_path = "service_account_key_generative_exam.json"
#     initialize_firebase(service_account_path)
#
#     # 初始化 Firestore 管理器
#     manager = FirestoreManager()
#
#     # 添加一個文檔
#     collection = "users"
#     document_id = "user_1"
#     user_data = {"name": "Alice", "age": 25, "email": "alice@example.com"}
#     print(manager.add_document(collection, user_data, document_id))
#
#     # 獲取文檔
#     print(manager.get_document(collection, document_id))
#
#     # 更新文檔
#     update_data = {"age": 26}
#     print(manager.update_document(collection, document_id, update_data))
#
#     # 刪除文檔
#     print(manager.delete_document(collection, document_id))
#
#     # 批量添加文檔
#     batch_data = [
#         {"name": "Bob", "age": 30, "email": "bob@example.com"},
#         {"name": "Charlie", "age": 35, "email": "charlie@example.com"},
#     ]
#     print(manager.batch_add_documents(collection, batch_data))
#
#     # 獲取集合中的所有文檔
#     print(manager.get_collection(collection))
