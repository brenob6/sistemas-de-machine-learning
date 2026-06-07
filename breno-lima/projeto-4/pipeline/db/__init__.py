from pymongo import MongoClient

uri = "mongodb://mongo:27017/"
client = MongoClient(uri)

DATABASE = "projeto-4"

database = client.get_database(DATABASE)
documents = database["documents"]

documents.create_index("sha256", unique=True)
documents.create_index("company")
documents.create_index("document_type")


def save_document(
    sha256: str, company: str, document_type: str, content: str, is_valid: bool
):
    document = {
        "sha256": sha256,
        "company": company,
        "document_type": document_type,
        "content": content,
        "is_valid": is_valid,
    }
    documents.insert_one(document)


def exists(sha256: str) -> bool:
    return documents.find_one({"sha256": sha256}, {"_id": 1}) is not None
