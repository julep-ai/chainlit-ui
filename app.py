import asyncio
import chainlit as cl
from julep import AsyncJulep
import os
import dotenv

dotenv.load_dotenv(override=True)

JULEP_API_KEY = os.getenv("JULEP_API_KEY")
AGENT_UUID = os.getenv("AGENT_UUID")

################################################################################

julep_client = AsyncJulep(api_key=JULEP_API_KEY, environment="dev")

session_id = None

@cl.on_chat_start
async def on_chat_start():
    global session_id

    session = await julep_client.sessions.create(
        agent=AGENT_UUID,
        system_template=None,
        recall_options={
            "mode": "hybrid",
            "num_search_messages": 4,
            "max_query_length": 1000,
            "confidence": 0.5,
            "alpha": 0.5,
            "limit": 10,
            "mmr_strength": 0.5,
        },
    )
    session_id = session.id

    print("Session created")

    await cl.Message(content="Hello, how can I help you today?").send()


@cl.on_message
async def on_message(message: cl.Message):
    # returned docs (response.docs)
    # if data frame, it's better

    async with cl.Step(name="Documents") as step:
        # Step is sent as soon as the context manager is entered
        global session_id
        response = await julep_client.sessions.chat(session_id=session_id,
                                                    messages=[{
                                                        "role":
                                                        "user",
                                                        "content":
                                                        message.content
                                                    }],
                                                    recall=True)

        docs = response.docs
        if docs:
            # Create elements for each document
            elements = []
            element_names = []

            for i, doc in enumerate(docs):
                title = doc.title if doc.title else f'Document {i+1}'
                # Create a sanitized name from the title (for reference)
                element_name = doc.title
                if len(element_name) > 16:
                    element_name = element_name[:16] + "..."
                element_names.append(element_name)

                # Add Text element with markdown content
                step.elements.append(
                    cl.Text(
                        name=element_name,
                        content=doc.snippet.content,
                        display="side"  # This will enable pagination
                    ))

            # Set the step's content directly and then update
            step.output = "Retrieved documents: " + ", ".join(element_names)
            await step.update()

        returned_content = response.choices[0].message.content

        await cl.Message(content=returned_content).send()
