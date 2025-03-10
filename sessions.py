import os
import dotenv

dotenv.load_dotenv(override=True)

agent_id = os.getenv("AGENT_UUID")

system_template1 = open("system-templates/system-template-1.jinja").read()
system_template2 = open("system-templates/system-template-2.jinja").read()
system_template3 = open("system-templates/system-template-3.jinja").read()
session_hybrid_mmr = {
    "agent": agent_id,
    "system_template": None,
    "recall_options": {
        "mode": "hybrid",
        "num_search_messages": 4,
        "max_query_length": 1000,
        "confidence": 0.7,
        "alpha": 0.5,
        "limit": 10,
        "mmr_strength": 0.7,
    },
}

session_vector = {
    "agent": agent_id,
    "system_template": None,
    "recall_options": {
        "mode": "vector",
        "num_search_messages": 4,
        "max_query_length": 1000,
        "confidence": 0.7,
        "limit": 10,
    },
}


sessions = {
    "Tia (Hybrid + MMR)": session_hybrid_mmr,
    "Tia (Vector)": session_vector,
}

system_templates = {
    "Tia 1 (professional)": system_template1,
    "Tia 2 (casual)": system_template2,
    "Tia 3 (casual + displays tables for product recommendations)": system_template3,
}
