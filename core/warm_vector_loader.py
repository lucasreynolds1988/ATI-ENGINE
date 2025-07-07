import json
import os

VECTOR_MEMORY_PATH = "memory/vector_memory.json"

def load_vectors():
    if not os.path.exists(VECTOR_MEMORY_PATH):
        return {}
    with open(VECTOR_MEMORY_PATH) as f:
        return json.load(f)

def get_vector_for_manual(manual_id):
    vectors = load_vectors()
    return vectors.get(manual_id, {})
