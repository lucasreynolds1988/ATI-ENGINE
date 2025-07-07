import os
import json

VECTOR_MEMORY_PATH = "memory/vector_memory.json"
ONTOLOGY_PATH = "memory/ontology_index.json"
AGENT_STATE_PATH = "memory/agent_state.json"

def load_warm_start_memory():
    memory = {}
    for path in [VECTOR_MEMORY_PATH, ONTOLOGY_PATH, AGENT_STATE_PATH]:
        if os.path.exists(path):
            with open(path, "r") as f:
                memory[os.path.basename(path)] = json.load(f)
    return memory
