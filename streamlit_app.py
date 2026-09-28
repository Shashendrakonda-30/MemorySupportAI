import os
import time
import streamlit as st

from dotenv import load_dotenv
from hindsight_client import Hindsight
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

hindsight_api_key = os.getenv("HINDSIGHT_API_KEY")
hindsight_base_url = os.getenv("HINDSIGHT_BASE_URL")
bank_id = os.getenv("HINDSIGHT_BANK_ID")

gemini_api_key = os.getenv("GEMINI_API_KEY")


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MemorySupport AI",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #666666;
        margin-bottom: 25px;
    }

    .memory-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f4f0ff;
        margin-bottom: 10px;
    }

    .insight-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f5f7fa;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CHECK SETTINGS
# ============================================================

if not hindsight_api_key:
    st.error("HINDSIGHT_API_KEY is missing from .env")
    st.stop()

if not hindsight_base_url:
    st.error("HINDSIGHT_BASE_URL is missing from .env")
    st.stop()

if not bank_id:
    st.error("HINDSIGHT_BANK_ID is missing from .env")
    st.stop()

if not gemini_api_key:
    st.error("GEMINI_API_KEY is missing from .env")
    st.stop()


# ============================================================
# CONNECT TO HINDSIGHT + GEMINI
# ============================================================

@st.cache_resource
def connect_services():

    hindsight = Hindsight(
        base_url=hindsight_base_url,
        api_key=hindsight_api_key
    )

    gemini = genai.Client(
        api_key=gemini_api_key
    )

    return hindsight, gemini


hindsight, gemini = connect_services()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "latest_memories" not in st.session_state:
    st.session_state.latest_memories = []

if "memory_used" not in st.session_state:
    st.session_state.memory_used = False

if "issue_count" not in st.session_state:
    st.session_state.issue_count = 0


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🧠 MemorySupport AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI Customer Support with Long-Term Memory'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR - CUSTOMER PROFILE
# ============================================================

with st.sidebar:

    st.header("👤 Customer Profile")

    customer_name = st.text_input(
        "Customer name",
        value="Rahul"
    )

    st.divider()

    st.subheader("🔌 System Status")

    st.success("Hindsight connected")
    st.success("Gemini connected")

    st.divider()

    st.subheader("📊 Session")

    st.metric(
        "Issues discussed",
        st.session_state.issue_count
    )

    if st.session_state.memory_used:

        st.success("🧠 Memory used")

    else:

        st.info("🧠 Waiting for memory")

    st.divider()

    st.info(
        """
        **How it works**

        1. Customer sends a message
        2. Hindsight recalls memories
        3. Gemini uses the memories
        4. AI generates a response
        5. Hindsight saves the interaction
        """
    )


# ============================================================
# CUSTOMER INSIGHTS
# ============================================================

st.subheader("🔎 Customer Insights")

if st.session_state.latest_memories:

    st.caption(
        "Information learned from the customer's long-term memory:"
    )

    memory_text = " ".join(
        st.session_state.latest_memories
    ).lower()


    # --------------------------------------------------------
    # DETECT OPERATING SYSTEM
    # --------------------------------------------------------

    if "windows 11" in memory_text:

        operating_system = "Windows 11"

    elif "windows" in memory_text:

        operating_system = "Windows"

    elif "macos" in memory_text or "mac os" in memory_text:

        operating_system = "macOS"

    elif "linux" in memory_text:

        operating_system = "Linux"

    else:

        operating_system = "Not known"


    # --------------------------------------------------------
    # DETECT BROWSER
    # --------------------------------------------------------

    if "google chrome" in memory_text or "chrome" in memory_text:

        browser = "Google Chrome"

    elif "firefox" in memory_text:

        browser = "Firefox"

    elif "edge" in memory_text:

        browser = "Microsoft Edge"

    elif "safari" in memory_text:

        browser = "Safari"

    else:

        browser = "Not known"


    # --------------------------------------------------------
    # DETECT KNOWN ISSUE
    # --------------------------------------------------------

    if "pdf" in memory_text:

        known_issue = "PDF Upload"

    elif "login" in memory_text or "log in" in memory_text:

        known_issue = "Login"

    elif "password" in memory_text:

        known_issue = "Password"

    else:

        known_issue = "Not known"


    insight_col1, insight_col2, insight_col3 = st.columns(3)


    with insight_col1:

        st.metric(
            "💻 Operating System",
            operating_system
        )


    with insight_col2:

        st.metric(
            "🌐 Browser",
            browser
        )


    with insight_col3:

        st.metric(
            "📄 Known Issue",
            known_issue
        )

else:

    st.info(
        "Customer insights will appear after "
        "Hindsight recalls customer memory."
    )


st.divider()


# ============================================================
# MAIN LAYOUT
# ============================================================

chat_column, memory_column = st.columns(
    [2.2, 1],
    gap="large"
)


# ============================================================
# CUSTOMER MEMORY PANEL
# ============================================================

with memory_column:

    st.subheader("🧠 Customer Memory")

    if st.session_state.latest_memories:

        st.caption(
            "Relevant memories recalled from Hindsight:"
        )

        for index, memory in enumerate(
            st.session_state.latest_memories,
            start=1
        ):

            st.markdown(
                f"""
                <div class="memory-box">
                <b>Memory {index}</b><br><br>
                {memory}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No memories have been recalled yet."
        )


    st.divider()


    # ========================================================
    # CURRENT SESSION
    # ========================================================

    st.subheader("📋 Current Session")

    if st.session_state.messages:

        user_messages = [
            message
            for message in st.session_state.messages
            if message["role"] == "user"
        ]

        if user_messages:

            for index, message in enumerate(
                user_messages,
                start=1
            ):

                st.markdown(
                    f"**Issue {index}:** "
                    f"{message['content']}"
                )

        else:

            st.caption(
                "No customer issues yet."
            )

    else:

        st.caption(
            "No conversation yet."
        )


# ============================================================
# CHAT AREA
# ============================================================

with chat_column:

    st.subheader("💬 Customer Support")


    # ========================================================
    # DISPLAY PREVIOUS CHAT
    # ========================================================

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )


    # ========================================================
    # CUSTOMER INPUT
    # ========================================================

    user_message = st.chat_input(
        "Describe your problem..."
    )


    if user_message:

        if not customer_name.strip():

            st.warning(
                "Please enter the customer name first."
            )

            st.stop()


        # ====================================================
        # SAVE USER MESSAGE TO SESSION
        # ====================================================

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        st.session_state.issue_count += 1


        with st.chat_message("user"):

            st.markdown(user_message)


        # ====================================================
        # HINDSIGHT RECALL
        # ====================================================

        with st.chat_message("assistant"):

            with st.spinner(
                "🧠 Searching long-term memory..."
            ):

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
- Operating system
- Browser
- Device information
- Previous support conversations
- Important customer details

Return memories that are useful for answering
the customer's current message.
"""
                    )

                    memories = []

                    if result.results:

                        for memory in result.results:

                            memories.append(
                                memory.text
                            )


                    st.session_state.latest_memories = memories


                    if memories:

                        memory_context = "\n".join(
                            memories
                        )

                        st.session_state.memory_used = True

                    else:

                        memory_context = (
                            "No previous memories found."
                        )

                        st.session_state.memory_used = False


                except Exception as e:

                    memory_context = (
                        "No previous memories available."
                    )

                    st.session_state.latest_memories = []

                    st.session_state.memory_used = False

                    st.warning(
                        "Memory recall temporarily failed."
                    )


            # =================================================
            # GEMINI PROMPT
            # =================================================

            prompt = f"""
You are MemorySupport AI, an intelligent
customer-support agent with long-term memory.

Customer name:
{customer_name}

Previous relevant memories:
{memory_context}

Current customer message:
{user_message}

Your job is to provide helpful customer support.

Rules:

- Use previous memories when they are relevant.
- If a previous solution worked, mention it.
- Personalize the response using remembered information.
- Do not invent memories.
- Do not claim something happened unless supported
  by the memories.
- Be polite and professional.
- Give clear and practical troubleshooting steps.
- Keep the answer reasonably concise.
"""


            # =================================================
            # GEMINI RESPONSE
            # =================================================

            with st.spinner(
                "🤖 Generating personalized response..."
            ):

                answer = None


                for attempt in range(3):

                    try:

                        response = (
                            gemini.models.generate_content(
                                model="gemini-3.8-flash",
                                contents=prompt
                            )
                        )

                        answer = response.text

                        break


                    except Exception:

                        if attempt < 2:

                            time.sleep(5)


            # =================================================
            # FALLBACK RESPONSE
            # =================================================

            if answer is None:

                if memories:

                    answer = f"""
Hello {customer_name},

Gemini is temporarily unavailable, but I can still
use your previous support history.

Based on your previous interactions:

{memory_context}

Please try the solution that worked previously.

If the problem continues, please tell me the exact
error message you are seeing and I can help you
troubleshoot further.
"""

                    st.warning(
                        "Gemini is temporarily unavailable. "
                        "Using Hindsight memory fallback."
                    )

                else:

                    answer = f"""
Hello {customer_name},

I'm temporarily unable to generate an AI response.

Please describe the exact problem or error you are
experiencing, and we can continue troubleshooting.
"""

                    st.warning(
                        "Gemini is temporarily unavailable."
                    )


            # =================================================
            # DISPLAY AI RESPONSE
            # =================================================

            st.markdown(answer)


            # =================================================
            # SAVE AI RESPONSE TO SESSION
            # =================================================

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


            # =================================================
            # SAVE INTERACTION TO HINDSIGHT
            # =================================================

            with st.spinner(
                "💾 Saving conversation to long-term memory..."
            ):

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

                        break


                    except Exception:

                        if attempt < 2:

                            time.sleep(5)


            # =================================================
            # SAVE STATUS
            # =================================================

            if memory_saved:

                st.success(
                    "🧠 Conversation saved to "
                    "long-term memory."
                )

            else:

                st.warning(
                    "Conversation could not be saved "
                    "this time."
                )