from pymongo import MongoClient

uri = "mongodb://mongo:27017/"
client = MongoClient(uri)

DATABASE = "projeto-4"

database = client.get_database(DATABASE)
documents = database["documents"]

documents.create_index("sha256", unique=True)
documents.create_index("company")
documents.create_index("document_type")


def find_documents_by_company(company: str):
    return list(documents.find({"company": company}, {"_id": 0}))


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
