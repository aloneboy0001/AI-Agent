import streamlit as st
import os
from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.generic_loader import load_content
from SimplerLLM.tools.json_helpers import extract_json_from_text

class Agent:
    def __init__(self, model_provider, model_name):
        self.llm_instance = LLM.create(model_provider, model_name=model_name)
        self.available_actions = {}
        self.system_prompt_template = """
You run in a loop of Thought, Action, PAUSE, Action_Response. At the end of the loop you output an Answer.
Use Thought to understand the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Action_Response will be the result of running those actions.
Your available actions are:
{actions_list}
To use an action, please use the following format:
Thought: Do I need to use a tool? Yes
Action:
{{
    "function_name": tool_name,
    "function_params": {{
        "param": "value"
    }}
}}
Action_Response: the result of the action
""".strip()

    def add_tool(self, tool_function):
        tool_name = tool_function.__name__
        description = tool_function.__doc__.strip()
        self.available_actions[tool_name] = {
            "function": tool_function,
            "description": description
        }

    def construct_system_prompt(self):
        actions_description = "\n".join(
            [f"{name}:\n {details['description']}" for name, details in self.available_actions.items()]
        )
        return self.system_prompt_template.format(actions_list=actions_description)

    def generate_response(self, user_query, max_turns=5):
        react_system_prompt = self.construct_system_prompt()
        messages = [
            {"role": "system", "content": react_system_prompt},
            {"role": "user", "content": user_query}
        ]
        turn_count = 1
        final_response = ""

        while turn_count <= max_turns:
            turn_count += 1
            agent_response = self.llm_instance.generate_response(messages=messages)
            messages.append({"role": "assistant", "content": agent_response})

            action_json = extract_json_from_text(agent_response)
            if action_json:
                function_name = action_json[0]['function_name']
                function_params = action_json[0]['function_params']
                if function_name not in self.available_actions:
                    raise Exception(f"Unknown action: {function_name}")
                action_function = self.available_actions[function_name]["function"]
                result = action_function(**function_params)
                function_result_message = f"Action_Response: {result}"
                messages.append({"role": "user", "content": function_result_message})
            else:
                final_response = agent_response
                break

        return final_response

def load_content_from_url(url: str):
    """Load the page content from a given URL."""
    content = load_content(url)
    return content.content

# Streamlit UI
st.set_page_config(page_title="Article Summarizer", layout="centered")
st.title("AI Article Summarizer")

url = st.text_input("Enter Article URL", "")
submit = st.button("Generate Summary")

if submit and url:
    with st.spinner("Generating summary..."):
        agent = Agent(LLMProvider.GEMINI, model_name="gemini-1.5-flash")
        agent.add_tool(load_content_from_url)

        user_query = f"""
        generate a concise bullet point summary of the following article:
        [{url}]({url})
        """
        response = agent.generate_response(user_query)
        st.subheader("Summary")
        st.markdown(response)
