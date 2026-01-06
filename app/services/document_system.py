class User:
    def __init__(self, user_id: int, name: str):
        self._id = user_id
        self._name = name

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name
class Document:
    def __init__(self, doc_id: int, title: str, owner: User):
        self._id = doc_id
        self._title = title
        self._owner = owner

    def get_id(self):
        return self._id

    def get_title(self):
        return self._title

    def get_owner(self):
        return self._owner
class DocumentStore:
    def __init__(self):
        self._documents = []

    def add_document(self, document: Document):
        self._documents.append(document)

    def get_documents_by_user(self, user: User):
        return [
            doc for doc in self._documents
            if doc.get_owner() == user
        ]
if __name__ == "__main__":
    # Create users
    user1 = User(1, "Alice")
    user2 = User(2, "Bob")

    # Create documents
    doc1 = Document(1, "Resume", user1)
    doc2 = Document(2, "Notes", user1)
    doc3 = Document(3, "Invoice", user2)

    # Create store and add documents
    store = DocumentStore()
    store.add_document(doc1)
    store.add_document(doc2)
    store.add_document(doc3)

    # Fetch documents for user1
    user1_docs = store.get_documents_by_user(user1)

    for doc in user1_docs:
        print(doc.get_title())
