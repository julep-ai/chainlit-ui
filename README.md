# Welcome to TIRA Beauty AI Assistant (Julep) ✨

TIRA Beauty AI Assistant is an intelligent beauty advisor built by Julep AI that helps you discover beauty products, understand ingredients, and get personalized beauty advice.

## Getting Started 🚀

1. **Select Search Options**: First, choose the AI agent with your preferred search capabilities
2. **Choose Conversation Style**: Select a system template that defines how the assistant will interact with you
3. **Start Chatting**: Ask questions about beauty products, ingredients, or get personalized recommendations!

## What You Can Do 💬

- **Discover Products**: Find beauty products from TIRA's catalog (~1K products)
- **Learn About Ingredients**: Get explanations about skincare and makeup ingredients
- **Get Personalized Advice**: Receive customized beauty and skincare routines
- **Compare Products**: Understand differences between similar items
- **Check Availability**: Get real-time product availability information

## Key Features 🔑

- **Smart Search**: Uses hybrid search combining vector and text-based approaches.
- **RAG Pipeline**: Leverages Retrieval-Augmented Generation to provide accurate, factual responses.
- **Product Knowledge**: Current deployed agent contains ~1K products.
- **Beauty Expertise**: Can explain ingredients, suggest routines, and compare products.
- **Real-time Data**: Integrates with TIRA's systems to check stock and availability.

## Technical Details 🔧

This assistant is powered by:

- **Julep AI** Builds the chatbot and orchestrates the conversation
- **Claude 3.7 Sonnet** as the base model for the chatbot.
- **Claude 3.5 Haiku / gpt-4o mini** for contextualization
- **openai text-embeddings-3-large** for embedding
- **Hybrid RAG Search** combining vector, BM25, and trigram search with MMR for diverse results
- **Automated product indexing and FAQ generation**

## Tips for Best Results 💡

- Be specific about your skin type, concerns, or preferences
- Ask about specific ingredients you're curious about
- Request personalized routines for your unique needs
- Compare similar products to find your perfect match

Enjoy your beauty consultation experience with TIRA Beauty AI Assistant!