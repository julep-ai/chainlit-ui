import os
import dotenv

dotenv.load_dotenv(override=True)

agent_id = os.getenv("AGENT_UUID")

session1 = {
    "agent": agent_id,
    "system_template": None,
    "recall_options": {
        "mode": "hybrid",
        "num_search_messages": 4,
        "max_query_length": 1000,
        "confidence": 0.5,
        "alpha": 0.5,
        "limit": 10,
        "mmr_strength": 0.5,
    },
}

session2 = {
    "agent": agent_id,
    "system_template": None,
    "recall_options": {
        "mode": "vector",
        "num_search_messages": 4,
        "max_query_length": 1000,
        "confidence": 0.5,
        "limit": 10,
    },
}


sessions = {
    "Main Agent": session1,
    "Plain Vector Agent": session2,
}

