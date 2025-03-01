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
DEFAULT_SYSTEM_TEMPLATE: str = '''You are an AI agent designed to assist users with their queries about products from Tira Beauty website.
Your goal is to provide clear and detailed responses.

**Guidelines**:
1. Assume the user is unfamiliar with the company and products.
2. Thoroughly read and comprehend the user's question.
3. Use the provided context documents to find relevant information.
4. Craft a detailed response based on the context and your understanding of the company and products.
5. Include links to specific website pages for further information when applicable.

**Response format**:
- Use simple, clear language.
- Include relevant website links.

**Important**:
- For questions related to the business, only use the information that are explicitly given in the documents above.
- If the user asks about the business, and it's not given in the documents above, respond with an answer that states that you don't know.
- Use the most recent and relevant data from context documents.
- Be proactive in helping users find solutions.
- Ask for clarification if the query is unclear.
- Inform users if their query is unrelated to the given website.
- Avoid using the following in your response: Based on the provided documents, based on the provided information, based on the documentation... etc.

{%- if docs -%}
{{NEWLINE}} Relevant documents: {{NEWLINE}}
  {%- for i, doc in enumerate(docs) -%}
    {{NEWLINE}}------------------------------------------------------------
Document {{i+1}}: {{NEWLINE}}
Name: {{ doc.title }}
    {%- if doc.content is string -%}
      {{NEWLINE}}Content: {{ doc.content }} {{NEWLINE}}
    {%- else -%}
      {%- for snippet in doc.content -%}
        {{NEWLINE}}Content: {{ snippet }} {{NEWLINE}}
      {%- endfor -%}
    {%- endif -%}
    {%- if doc.metadata -%}
      Product Details: {{NEWLINE}}
      {%- if doc.metadata.brand.name -%}
      Brand: {{ doc.metadata.brand.name }} {{NEWLINE}}
      {%- endif -%}
      {%- if doc.metadata.slug -%}
      URL: https://www.tirabeauty.com/product/{{ doc.metadata.slug }} {{NEWLINE}}
      {%- endif -%}
      {%- if doc.metadata.price and doc.metadata.price.min and doc.metadata.price.currency -%}
      Price: {{ doc.metadata.price.min }} {{ doc.metadata.price.currency }} {{NEWLINE}}
      {%- endif -%}
      {%- if doc.metadata.rating -%}
      Rating: {{ doc.metadata.rating }} {{NEWLINE}}
      {%- endif -%}
      {%- if doc.metadata.categories and doc.metadata.categories[0].name -%}
      Categories: {{ doc.metadata.categories[0].name }} {{NEWLINE}}
      {%- endif -%}
      {%- if doc.metadata.country_of_origin -%}
      Country of Origin: {{ doc.metadata.country_of_origin }} {{NEWLINE}}
      {%- endif -%}
      {%- if doc.metadata.tags -%}
      Tags: {{ doc.metadata.tags | join(', ') }} {{NEWLINE}}
      {%- endif -%}
      {%- if doc.metadata.attributes.skin_type -%}
      Skin Type: {{ doc.metadata.attributes.skin_type }} {{NEWLINE}}
      {%- endif -%}
      {%- if doc.metadata.attributes.gender -%}
      Gender: {{ doc.metadata.attributes.gender }} {{NEWLINE}}
      {%- endif -%}
      {%- if doc.metadata.attributes.discount -%}
      Discount: {{ doc.metadata.attributes.discount }} {{NEWLINE}}
      {%- endif -%}
      {%- if doc.metadata.attributes.benefits -%}
      Benefits: {{ doc.metadata.attributes.benefits | join(', ') }} {{NEWLINE}}
      {%- endif -%}
      {%- if doc.metadata.attributes.concern -%}
      Concerns: {{ doc.metadata.attributes.concern | join(', ') }} {{NEWLINE}}
      {%- endif -%}
      {%- if doc.metadata.attributes.formulation -%}
      Formulation: {{ doc.metadata.attributes.formulation }} {{NEWLINE}}
      {%- endif -%}
      {%- if doc.metadata.attributes['super-ingredients'] -%}
      Super-ingredients: {{ doc.metadata.attributes['super-ingredients'] | join(', ') }} {{NEWLINE}}
      {%- endif -%}
      {%- if doc.metadata.attributes.preference -%}
      Preferences: {{ doc.metadata.attributes.preference | join(', ') }} {{NEWLINE}}
      {%- endif -%}
      {%- if doc.metadata.attributes['shelf-life-in-months'] -%}
      Shelf Life: {{ doc.metadata.attributes['shelf-life-in-months'] }} months
      {%- endif -%}
    {%- endif -%}
  {%- endfor -%}
{%- endif -%}
'''


@cl.on_chat_start
async def on_chat_start():
    global session_id

    session = await julep_client.sessions.create(
        agent=AGENT_UUID,
        system_template=DEFAULT_SYSTEM_TEMPLATE,
        recall_options={
            "mode": "hybrid",
            "num_search_messages": 4,
            "max_query_length": 800,
            "confidence": -0.9,
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
                    )
                )
            
            # Set the step's content directly and then update
            step.output = "Retrieved documents: " + ", ".join(element_names)
            await step.update()

        returned_content = response.choices[0].message.content

        await cl.Message(content=returned_content).send()
