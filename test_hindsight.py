
    client.retain(
        bank_id=bank_id,
        content="""
Customer Rahul uses Windows 11 and Google Chrome.
Rahul previously had a PDF upload error.
Clearing the browser cache solved the problem.
"""
    )

    print("Memory stored successfully!")

    result = client.recall(
        bank_id="MemorySupportAI",
        content="this is a test memory."
        query="What problem did Rahul have previously and what solution worked?"
    )

    print("\n===== RECALLED MEMORIES =====")

    if not result.results:
        print("No memories found.")
    else:
        for memory in result.results:
            print(memory.text)

finally:
    client.close()

print("\n===== TEST COMPLETE =====")import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

api_key = os.getenv("HINDSIGHT_API_KEY")
base_url = os.getenv("HINDSIGHT_BASE_URL")
bank_id = os.getenv("HINDSIGHT_BANK_ID")

print("Starting Hindsight test...")

if not api_key:
    print("ERROR: API key is missing")
    exit()

if not bank_id:
    print("ERROR: Bank ID is missing")
    exit()

print("API key found")
print("Bank ID:", bank_id)

client = Hindsight(
    base_url=base_url,
    api_key=HINDSIGHT_API_KEY
)

try:
    print("Connected to Hindsight!")