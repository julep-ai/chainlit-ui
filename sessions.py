import os
import dotenv

dotenv.load_dotenv(override=True)

agent_id = os.getenv("AGENT_UUID")

system_template1 = open("system-templates/system-template-1.jinja").read()
system_template2 = open("system-templates/system-template-2.jinja").read()

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

system_templates = {
    "Default System Template": system_template1,
    "Modified System Template": system_template2,
}