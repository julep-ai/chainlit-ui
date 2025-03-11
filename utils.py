import chainlit as cl
from uuid import uuid4


def get_or_create_session_id():
    # Try to get existing session ID from user session
    session_id = cl.user_session.get("julep_session_id")

    if not session_id:
        # Generate new session ID if not exists
        session_id = str(uuid4())
        # Store in user session
        cl.user_session.set("julep_session_id", session_id)

    return session_id
