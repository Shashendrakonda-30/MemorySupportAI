import os
import time

from dotenv import load_dotenv
from hindsight_client import Hindsight
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

# Hindsight
hindsight_api_key = os.getenv("HINDSIGHT_API_KEY")
hindsight_base_url = os.getenv("HINDSIGHT_BASE_URL")
bank_id = os.getenv("HINDSIGHT_BANK_ID")

# Gemini
gemini_api_key = os.getenv("GEMINI_API_KEY")


# ============================================================
# CHECK SETTINGS
# ============================================================

if not hindsight_api_key:
    print("ERROR: HINDSIGHT_API_KEY is missing")
    exit()

if not hindsight_base_url:
    print("ERROR: HINDSIGHT_BASE_URL is missing")
    exit()

if not bank_id:
    print("ERROR: HINDSIGHT_BANK_ID is missing")
    exit()

if not gemini_api_key:
    print("ERROR: GEMINI_API_KEY is missing")
    exit()


# ============================================================
# CONNECT TO HINDSIGHT
# ============================================================

hindsight = Hindsight(
    base_url=hindsight_base_url,
    api_key=hindsight_api_key
)


# ============================================================
# CONNECT TO GEMINI
# ============================================================

gemini = genai.Client(
    api_key=gemini_api_key
)


# ============================================================
# APPLICATION START
# ============================================================

print("=" * 50)
print("          MEMORYSUPPORT AI")
print("=" * 50)

print("Hindsight connected!")
print("Gemini connected!")
print()


# ============================================================
# CUSTOMER NAME
# ============================================================

customer_name = input("Enter customer name: ").strip()

print()
print("Start chatting with MemorySupport AI.")
print("Type 'exit' to stop.")
print()


# ============================================================
# MAIN CHAT LOOP
# ============================================================

while True:

    user_message = input("Customer: ").strip()

    # Exit
    if user_message.lower() == "exit":
        break

    # Ignore empty messages
    if not user_message:
        continue


    # ========================================================
    # STEP 1: RECALL CUSTOMER MEMORY
    # ========================================================

    print()
    print("[Searching customer memory...]")

    try:

        result = hindsight.recall(
            bank_id=bank_id,
            query=f"""
Customer name: {customer_name}

Current customer problem:
{user_message}

Find relevant previous information about this customer.

Look for:
- Previous problems
- Previous solutions
- Customer preferences
- Device information
- Browser information
- Previous support conversations
- Important customer details
"""
        )

        memories = []

        if result.results:

            for memory in result.results:
                memories.append(memory.text)

        if memories:

            memory_context = "\n".join(memories)

            print("[Previous memory found]")

        else:

            memory_context = "No previous memories found."

            print("[No previous memory found]")

    except Exception as e:

        print("Memory recall error:", e)

        memory_context = "No previous memories available."


    # ========================================================
    # STEP 2: CREATE GEMINI PROMPT
    # ========================================================

    prompt = f"""
You are MemorySupport AI, an intelligent customer-support agent.

Customer name:
{customer_name}

Previous relevant memories:
{memory_context}

Current customer message:
{user_message}

Your job is to provide helpful customer support.

Rules:
- Use previous memories when they are relevant.
- If a previous solution worked, mention it when appropriate.
- Do not invent memories.
- Do not claim something happened unless supported by the memories.
- Be polite and professional.
- Give clear and practical troubleshooting steps.
- Keep the answer reasonably concise.
"""


    # ========================================================
    # STEP 3: GENERATE GEMINI RESPONSE
    # ========================================================

    print("[Generating AI response...]")

    answer = None

    for attempt in range(3):

        try:

            response = gemini.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            answer = response.text

            break

        except Exception as e:

            print(
                f"Gemini attempt {attempt + 1}/3 failed."
            )

            print("Error:", e)

            if attempt < 2:

                print("Waiting 5 seconds before retry...")
                time.sleep(5)

            else:

                print()
                print(
                    "Gemini is currently unavailable."
                )

                print(
                    "Please try your message again."
                )


    # If Gemini failed
    if answer is None:

        print()

        continue


    # ========================================================
    # STEP 4: DISPLAY RESPONSE
    # ========================================================

    print()
    print("MemorySupport AI:")
    print(answer)
    print()


    # ========================================================
    # STEP 5: SAVE INTERACTION TO HINDSIGHT
    # ========================================================

    print("[Saving conversation to memory...]")

    memory_saved = False

    for attempt in range(3):

        try:

            hindsight.retain(
                bank_id=bank_id,
                content=f"""
Customer: {customer_name}

Customer message:
{user_message}

MemorySupport AI response:
{answer}
"""
            )

            memory_saved = True

            print("[Memory saved successfully]")
            print()

            break

        except Exception as e:

            print(
                f"Memory save attempt {attempt + 1}/3 failed."
            )

            print("Error:", e)

            if attempt < 2:

                print("Waiting 5 seconds before retry...")
                time.sleep(5)


    if not memory_saved:

        print("[Memory could not be saved this time]")
        print()


# ============================================================
# CLOSE HINDSIGHT
# ============================================================

hindsight.close()


# ============================================================
# APPLICATION STOPPED
# ============================================================

print()
print("=" * 50)
print("       MemorySupport AI stopped.")
print("=" * 50)