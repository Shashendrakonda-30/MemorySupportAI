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


def get_secret(name, default=None):
    """
    Get value from Streamlit Secrets first,
    then from .env / environment variables.
    """

    try:
        value = st.secrets.get(name)

        if value:
            return value

    except Exception:
        pass

    return os.getenv(name, default)


# ============================================================
# SETTINGS
# ============================================================

HINDSIGHT_API_KEY = get_secret("HINDSIGHT_API_KEY")

HINDSIGHT_BASE_URL = get_secret(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io"
)

HINDSIGHT_BANK_ID = get_secret(
    "HINDSIGHT_BANK_ID",
    "MemorySupport AI"
)

GEMINI_API_KEY = get_secret("GEMINI_API_KEY")

# You can change this in .env later if required.
GEMINI_MODEL = get_secret(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


# ============================================================
# PAGE CONFIG
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

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CHECK API SETTINGS
# ============================================================

if not HINDSIGHT_API_KEY:

    st.error(
        "❌ HINDSIGHT_API_KEY is missing."
    )

    st.stop()


if not GEMINI_API_KEY:

    st.error(
        "❌ GEMINI_API_KEY is missing."
    )

    st.stop()


# ============================================================
# CONNECT TO SERVICES
# ============================================================

@st.cache_resource
def connect_services():

    hindsight = Hindsight(
        base_url=HINDSIGHT_BASE_URL,
        api_key=HINDSIGHT_API_KEY
    )

    gemini = genai.Client(
        api_key=GEMINI_API_KEY
    )

    return hindsight, gemini


try:

    hindsight, gemini = connect_services()

    hindsight_connected = True
    gemini_connected = True

except Exception as e:

    hindsight_connected = False
    gemini_connected = False

    st.error(
        f"❌ Could not connect to services:\n\n{e}"
    )

    st.stop()


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


if "last_gemini_error" not in st.session_state:

    st.session_state.last_gemini_error = ""


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
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("👤 Customer Profile")

    customer_name = st.text_input(
        "Customer name",
        value="Rahul"
    )

    st.divider()

    st.subheader("🔌 System Status")

    if hindsight_connected:

        st.success("Hindsight connected")

    else:

        st.error("Hindsight disconnected")


    if gemini_connected:

        st.success("Gemini connected")

    else:

        st.error("Gemini disconnected")


    st.caption(
        f"Gemini model: `{GEMINI_MODEL}`"
    )

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

    st.subheader("ℹ️ How it works")

    st.info(
        """
        **1. Customer sends a message**

        ↓

        **2. Hindsight recalls previous memories**

        ↓

        **3. Gemini receives the memories**

        ↓

        **4. AI generates a personalized response**

        ↓

        **5. Conversation is saved to Hindsight**
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
    # OPERATING SYSTEM
    # --------------------------------------------------------

    if "windows 11" in memory_text:

        operating_system = "Windows 11"

    elif "windows" in memory_text:

        operating_system = "Windows"

    elif (
        "macos" in memory_text
        or "mac os" in memory_text
    ):

        operating_system = "macOS"

    elif "linux" in memory_text:

        operating_system = "Linux"

    else:

        operating_system = "Not known"


    # --------------------------------------------------------
    # BROWSER
    # --------------------------------------------------------

    if (
        "google chrome" in memory_text
        or "chrome" in memory_text
    ):

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
    # KNOWN ISSUE
    # --------------------------------------------------------

    if "pdf" in memory_text:

        known_issue = "PDF Upload"

    elif (
        "login" in memory_text
        or "log in" in memory_text
    ):

        known_issue = "Login"

    elif "password" in memory_text:

        known_issue = "Password"

    else:

        known_issue = "Not known"


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "💻 Operating System",
            operating_system
        )


    with col2:

        st.metric(
            "🌐 Browser",
            browser
        )


    with col3:

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
# MEMORY PANEL
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


    # --------------------------------------------------------
    # CURRENT SESSION
    # --------------------------------------------------------

    st.subheader("📋 Current Session")


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
            "No conversation yet."
        )


# ============================================================
# CHAT AREA
# ============================================================

with chat_column:

    st.subheader("💬 Customer Support")


    # --------------------------------------------------------
    # DISPLAY PREVIOUS CHAT
    # --------------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # --------------------------------------------------------
    # CUSTOMER INPUT
    # --------------------------------------------------------

    user_message = st.chat_input(
        "Describe your problem..."
    )


    if user_message:

        # ====================================================
        # CHECK CUSTOMER NAME
        # ====================================================

        if not customer_name.strip():

            st.warning(
                "Please enter the customer name first."
            )

            st.stop()


        # ====================================================
        # SAVE USER MESSAGE
        # ====================================================

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        st.session_state.issue_count += 1


        with st.chat_message("user"):

            st.markdown(
                user_message
            )


        # ====================================================
        # IMPORTANT INITIALIZATION
        # ====================================================
        #
        # These MUST exist even if Hindsight fails.
        #

        memories = []

        memory_context = (
            "No previous memories available."
        )


        # ====================================================
        # HINDSIGHT RECALL
        # ====================================================

        with st.chat_message("assistant"):

            with st.spinner(
                "🧠 Searching long-term memory..."
            ):

                try:

                    result = hindsight.recall(

                        bank_id=HINDSIGHT_BANK_ID,

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


                    # ------------------------------------------------
                    # EXTRACT MEMORIES
                    # ------------------------------------------------

                    if result.results:

                        for memory in result.results:

                            if memory.text:

                                memories.append(
                                    memory.text
                                )


                    st.session_state.latest_memories = memories


                    # ------------------------------------------------
                    # CREATE MEMORY CONTEXT
                    # ------------------------------------------------

                    if memories:

                        memory_context = "\n\n".join(
                            memories
                        )

                        st.session_state.memory_used = True

                    else:

                        memory_context = (
                            "No previous memories found."
                        )

                        st.session_state.memory_used = False


                except Exception as e:

                    memories = []

                    memory_context = (
                        "No previous memories available."
                    )

                    st.session_state.latest_memories = []

                    st.session_state.memory_used = False


                    st.warning(
                        "⚠️ Hindsight memory recall failed."
                    )

                    st.caption(
                        f"Technical details: {e}"
                    )


            # ====================================================
            # GEMINI PROMPT
            # ====================================================

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

IMPORTANT RULES:

1. Use previous memories when they are relevant.

2. If a previous solution worked, mention it.

3. Personalize the response using remembered information.

4. Do not invent memories.

5. Do not claim something happened unless supported
   by the memories.

6. Be polite and professional.

7. Give clear and practical troubleshooting steps.

8. If the customer has experienced the same problem
   before, explicitly connect the current problem
   with the previous interaction.

9. Keep the answer reasonably concise.

10. Address the customer by name when appropriate.
"""


            # ====================================================
            # GEMINI GENERATION
            # ====================================================

            answer = None

            gemini_error = None


            with st.spinner(
                "🤖 Generating personalized response..."
            ):

                # -----------------------------------------------
                # RETRY 3 TIMES
                # -----------------------------------------------

                for attempt in range(3):

                    try:

                        response = (
                            gemini.models.generate_content(
                                model=GEMINI_MODEL,
                                contents=prompt
                            )
                        )


                        if response is not None:

                            answer = response.text


                        if answer:

                            st.session_state.last_gemini_error = ""

                            break


                        else:

                            gemini_error = (
                                "Gemini returned an empty response."
                            )


                    except Exception as e:

                        gemini_error = str(e)

                        st.session_state.last_gemini_error = (
                            str(e)
                        )


                        # -------------------------------------------
                        # SHOW ACTUAL ERROR
                        # -------------------------------------------

                        if attempt == 0:

                            st.warning(
                                "⚠️ Gemini attempt 1 failed."
                            )

                            st.caption(
                                f"Error: {e}"
                            )


                        elif attempt == 1:

                            st.warning(
                                "⚠️ Gemini attempt 2 failed."
                            )

                            st.caption(
                                f"Error: {e}"
                            )


                        # -------------------------------------------
                        # RETRY WITH BACKOFF
                        # -------------------------------------------

                        if attempt < 2:

                            wait_time = 2 ** (
                                attempt + 1
                            )

                            time.sleep(
                                wait_time
                            )


            # ====================================================
            # GEMINI FAILED
            # ====================================================

            if answer is None:

                # -----------------------------------------------
                # MEMORY FALLBACK
                # -----------------------------------------------

                if memories:

                    answer = f"""
Hello {customer_name},

Gemini is temporarily unavailable, but I can still
use your previous support history.

I found that you previously had a similar problem:

{memory_context}

Since clearing the browser cache helped previously,
please try that again first.

If the problem continues, please tell me the exact
error message you are seeing.
"""


                    st.warning(
                        "⚠️ Gemini could not generate a response. "
                        "Using Hindsight memory fallback."
                    )


                    # -------------------------------------------
                    # SHOW ACTUAL GEMINI ERROR
                    # -------------------------------------------

                    if gemini_error:

                        with st.expander(
                            "🔧 Gemini technical error"
                        ):

                            st.code(
                                gemini_error
                            )


                else:

                    answer = f"""
Hello {customer_name},

I'm temporarily unable to generate an AI response.

Please describe the exact error message you are
experiencing and I will help you troubleshoot it.
"""


                    st.warning(
                        "⚠️ Gemini could not generate a response."
                    )


                    if gemini_error:

                        with st.expander(
                            "🔧 Gemini technical error"
                        ):

                            st.code(
                                gemini_error
                            )


            # ====================================================
            # DISPLAY FINAL ANSWER
            # ====================================================

            st.markdown(
                answer
            )


            # ====================================================
            # SAVE AI RESPONSE TO SESSION
            # ====================================================

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


            # ====================================================
            # SAVE INTERACTION TO HINDSIGHT
            # ====================================================

            memory_saved = False

            with st.spinner(
                "💾 Saving conversation to long-term memory..."
            ):

                for attempt in range(3):

                    try:

                        hindsight.retain(

                            bank_id=HINDSIGHT_BANK_ID,

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


                    except Exception as e:

                        if attempt < 2:

                            time.sleep(
                                2 ** (attempt + 1)
                            )


            # ====================================================
            # SAVE STATUS
            # ====================================================

            if memory_saved:

                st.success(
                    "🧠 Conversation saved to long-term memory."
                )

            else:

                st.warning(
                    "⚠️ Conversation could not be saved "
                    "to Hindsight this time."
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🧠 MemorySupport AI • Powered by Hindsight + Gemini"
)