import streamlit as st
import os
import requests
import json # For formatting observation output
from dotenv import load_dotenv

# LangChain components
from langchain_groq import ChatGroq
from langchain.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser # Helpful for parsing

# --- Callback Handler for Structured Agent Steps ---
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.agents import AgentAction, AgentFinish

class AgentStepsCallbackHandler(BaseCallbackHandler):
    """Callback Handler that prints agent actions and tool outputs to Streamlit."""

    def __init__(self, container):
        self.container = container
        self.steps = [] # Store steps chronologically

    def _render_steps(self):
        """Render the stored steps into the Streamlit container."""
        log_content = ""
        for step in self.steps:
            log_content += step.strip() + "\n\n" # Add separation between steps
        self.container.markdown(f"```text\n{log_content}\n```") # Use a text block for consistent formatting

    def on_agent_action(self, action: AgentAction, **kwargs) -> None:
        """Run when agent takes an action."""
        # action.log usually contains the full Thought + Action + Action Input block
        formatted_log = action.log.strip()
        # Add a separator if the log doesn't end nicely
        if not formatted_log.endswith("\n"):
             formatted_log += "\n---"
        self.steps.append(formatted_log)
        self._render_steps()


    def on_tool_end(self, output: str, name: str, **kwargs) -> None:
        """Run when tool ends running."""
        # Format the observation nicely
        try:
            # Try to parse as JSON for pretty printing if it's structured data
            parsed_output = json.dumps(json.loads(output), indent=2)
        except json.JSONDecodeError:
            # Otherwise, just use the raw string output
            parsed_output = output

        observation_step = f"Observation (from tool {name}):\n{parsed_output}\n---"
        self.steps.append(observation_step)
        self._render_steps()

    def on_agent_finish(self, finish: AgentFinish, **kwargs) -> None:
        """Run when agent finishes."""
        # The final thought and answer are often in finish.log or return_values
        # We'll let the main app display the final 'output' for clarity,
        # but we can add a marker here.
        finish_step = f"Thought:\n{finish.log.strip()}" # Often contains the final thought
        self.steps.append(finish_step)
        self.steps.append("\n🏁 Agent Finished")
        self._render_steps()

# --- Environment and API Key Setup ---
# Load local .env file if it exists (for local development)
load_dotenv()

st.set_page_config(page_title="Weather & Search Agent", layout="wide")
st.title("🌦️ Weather & Search Agent")
st.markdown("Ask me about weather, general knowledge, or tasks requiring both!")

# --- Sidebar for API Key Configuration ---
st.sidebar.header("API Configuration")
st.sidebar.markdown("""
Enter your API keys below. You can get them from:
- [Groq Cloud](https://console.groq.com/keys)
- [Weatherstack](https://weatherstack.com/) (Free tier available)
- [Tavily AI](https://tavily.com/) (Free tier available)
""")

groq_api_key_input = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    placeholder="gsk_...",
    help="Required for the LLM.",
    value=os.getenv("GROQ_API_KEY", "") # Load from .env if available
)

weather_api_key_input = st.sidebar.text_input(
    "Weatherstack API Key",
    type="password",
    placeholder="your_weatherstack_key",
    help="Required for the Get Weather tool.",
    value=os.getenv("WEATHER_API", "") # Load from .env if available
)

tavily_api_key_input = st.sidebar.text_input(
    "Tavily API Key",
    type="password",
    placeholder="tvly-...",
    help="Required for the Search tool.",
    value=os.getenv("TAVILY_API_KEY", "") # Load from .env if available
)

# Check if all keys are provided
all_keys_provided = groq_api_key_input and weather_api_key_input and tavily_api_key_input

if not all_keys_provided:
    st.warning("Please enter all required API keys in the sidebar to activate the agent.")
    st.stop() # Stop execution if keys are missing

# --- Tool Definition ---
@tool
def get_weather_data(city: str) -> str:
    """
    Fetches the current weather data for a given city using the Weatherstack API.
    Args:
        city (str): The name of the city for which to get weather data.
    Returns:
        str: A JSON string containing the weather data or an error message.
    """
    api_key = weather_api_key_input
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Return the raw JSON text, the callback will format it
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# --- Agent Setup (only if keys are provided) ---
try:
    llm = ChatGroq(
        model_name="llama3-70b-8192",
        groq_api_key=groq_api_key_input,
        temperature=0,
    )

    os.environ["TAVILY_API_KEY"] = tavily_api_key_input
    search_tool = TavilySearchResults(max_results=3)

    tools = [search_tool, get_weather_data]

    prompt = hub.pull("hwchase17/react") # Default ReAct prompt

    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False, # Crucial: Let the callback handle output, not AgentExecutor's verbose
        handle_parsing_errors=True,
        max_iterations=10,
    )

except Exception as e:
    st.error(f"Error initializing the agent components: {e}")
    st.stop()

# --- Main Interaction Area ---
user_query = st.text_input("Enter your question:", placeholder="e.g., What's the weather like in Paris today?")

if st.button("Run Agent", disabled=not all_keys_provided):
    if not user_query:
        st.warning("Please enter a question.")
    else:
        st.markdown("--- Agent Working... ---")
        # Container to display agent steps from the callback
        thinking_container = st.container()
        thinking_container.markdown("*(Agent steps will appear below)*")

        try:
            # Initialize the NEW callback handler, passing the container
            st_callback = AgentStepsCallbackHandler(thinking_container)

            # Invoke the agent with the callback
            response = agent_executor.invoke(
                {"input": user_query},
                {"callbacks": [st_callback]} # Pass the callback handler
            )

            # Display the final answer separately after the agent is done
            st.markdown("---") # Separator
            st.success("Final Answer:")
            st.markdown(response.get('output', 'No output generated.'))

        except Exception as e:
            st.error(f"An error occurred while running the agent: {e}")
            thinking_container.error("Agent stopped due to error.") # Update the container state