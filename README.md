# 🧠 MemorySupport AI

## AI Customer Support with Long-Term Memory

MemorySupport AI is an intelligent customer-support agent that uses
Hindsight long-term memory to remember previous customer interactions
and provide personalized support.

## Problem

Traditional AI customer-support systems often treat every conversation
as a new conversation.

This causes customers to repeatedly explain:

- Their previous problems
- Their device
- Their browser
- Previous solutions
- Their preferences

MemorySupport AI solves this by giving the AI long-term memory.

## Solution

The system uses:

- Hindsight for long-term memory
- Google Gemini for AI responses
- Streamlit for the web interface

## How It Works

Customer
    ↓
Streamlit Chat Interface
    ↓
Hindsight Recall
    ↓
Relevant Customer Memories
    ↓
Google Gemini
    ↓
Personalized Support Response
    ↓
Hindsight Retain
    ↓
Memory available for future conversations

## Key Features

### 1. Long-Term Customer Memory

Hindsight stores previous customer interactions.

### 2. Memory Recall

When a customer returns, the system searches their previous
interactions for relevant information.

### 3. Personalized Responses

Gemini uses recalled memories to generate personalized support.

### 4. Customer Profile

The interface displays information learned about the customer.

### 5. Memory Visualization

The application shows the memories retrieved from Hindsight.

### 6. Fault Tolerance

Temporary Gemini or Hindsight failures are handled using retries
and a memory-based fallback.

## Example

Customer:

"I am unable to upload a PDF again."

MemorySupport AI remembers:

- The customer previously had a PDF upload problem.
- The customer uses Google Chrome.
- Clearing the browser cache previously solved the problem.

The AI can therefore provide a personalized response instead of
starting the troubleshooting process from zero.

## Technology Stack

Python  
Streamlit  
Hindsight  
Google Gemini  
python-dotenv

## Project Structure

MemorySupportAI/
│
├── app.py
├── streamlit_app.py
├── test_hindsight.py
├── requirements.txt
├── README.md
├── .env
└── venv/

## Important

API keys are stored in `.env` and should never be committed to GitHub.

Example `.env`:

HINDSIGHT_API_KEY=your_key
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
HINDSIGHT_BANK_ID=MemorySupport AI
GEMINI_API_KEY=your_key