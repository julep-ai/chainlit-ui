import asyncio
import chainlit as cl
from julep import AsyncJulep
import os
import dotenv
from sessions import sessions, system_templates

dotenv.load_dotenv(override=True)

JULEP_API_KEY = os.getenv("JULEP_API_KEY")
AGENT_UUID = os.getenv("AGENT_UUID")

################################################################################

julep_client = AsyncJulep(api_key=JULEP_API_KEY, environment="dev")

session_id = None

@cl.on_chat_start
async def on_chat_start():
    global session_id
    
    # Create actions for each agent
    agent_actions = [
        cl.Action(
            name=agent_name, 
            payload=agent_values, 
            label=agent_name
        )
        for agent_name, agent_values in sessions.items()
    ]
    
    # Ask user to select an agent
    res = await cl.AskActionMessage(
        content="Please select an agent to chat with:",
        actions=agent_actions,
    ).send()
    
    print(res)

    if res:
        selected_settings = res["payload"]
    else:
        # Fallback to default if no selection
        selected_settings = sessions["Main Agent"]
    
    system_template_actions = [
        cl.Action(
            name=system_template_name,
            payload={"system_template": system_template_value},
            label=system_template_name
        )
        for system_template_name, system_template_value in system_templates.items()
    ]

    res = await cl.AskActionMessage(
        content="Please select a system template:",
        actions=system_template_actions,
    ).send()

    if res:
        selected_system_template = res["payload"]["system_template"]
    else:
        selected_system_template = None

    selected_settings["system_template"] = selected_system_template

    # Create session with selected agent
    session = await julep_client.sessions.create(
        **selected_settings
    )
    session_id = session.id

    print(f"Session created with agent settings: {selected_settings}")

    await cl.Message(content="Hello, how can I help you today?").send()


@cl.on_message
async def on_message(message: cl.Message):
    # returned docs (response.docs)
    # if data frame, it's better

    async with cl.Step(name="Documents") as step:
        # Step is sent as soon as the context manager is entered
        global session_id
        response = await julep_client.sessions.chat(
            session_id=session_id,
            messages=[{
                "role": "user",
                "content": message.content
                }],
            model="claude-3.7-sonnet",
            recall=True,
        )

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
