import requests

BASE_URL = "http://localhost:8001"

def test_embedding():
    response = requests.post(
        f"{BASE_URL}/embedding/",
        json={
            "input": ["This is a test sentence.", "And another one."]
        }
    )
    print("Embedding Test:")
    print(response.json())

def test_vector_db():
    # 创建集合
    requests.post(
        f"{BASE_URL}/vector-db/collections",
        json={"name": "test_collection"}
    )
    
    # 添加文档
    add_response = requests.post(
        f"{BASE_URL}/vector-db/documents",
        json={
            "collection_name": "test_collection",
            "documents": ["Document content 1", "Document content 2"],
            "ids": ["doc1", "doc2"]
        }
    )
    print("Add Documents:")
    print(add_response.json())
    
    # 查询
    query_response = requests.post(
        f"{BASE_URL}/vector-db/query",
        json={
            "collection_name": "test_collection",
            "query_texts": ["content"],
            "n_results": 1
        }
    )
    print("Query Results:")
    print(query_response.json())

def test_llm():
    response = requests.post(
        f"{BASE_URL}/llm/chat",
        json={
            "messages": [
                {"role": "user", "content": "Hello!"}
            ]
        }
    )
    print("LLM Chat Test:")
    print(response.json())

if __name__ == "__main__":
    test_embedding()
    test_vector_db()
    test_llm()
