import os
from langchain_classic import hub
from langchain_groq import ChatGroq
from langchain_classic.agents import create_react_agent,Tool,AgentExecutor
from langchain_experimental.utilities import PythonREPL
from langchain_community.utilities import GoogleSerperAPIWrapper

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY=os.getenv("api_key")
SERPER_API_KEY=os.getenv("SERPER_API_KEY")

groq_llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    temperature=0


)

python_repl=PythonREPL()
# checling of the tools working correctly


repl_tool=Tool(
    name="python_tool",
    description=(
        "a pyhton shell to execute the python commands"
        "Input should be a valid python queries"
    ),
    func=python_repl.run
)




google_serper=GoogleSerperAPIWrapper()



serper_tool=Tool(
    name="Google",
    description=(
        "a tool used to serve on google " 
        "input should be a string"
    ),
    func=google_serper.run
)



# Pulling the system prompt for the reAct agent
# Manually define the ReAct template
from langchain_classic.prompts import PromptTemplate
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
Thought: {agent_scratchpad}"""

react_prompt = PromptTemplate.from_template(template)

react_agent=create_react_agent(
    llm=groq_llm,
    tools=[repl_tool,serper_tool],
    prompt=react_prompt
)

def main():
    # Step 1: read keys, create groq_llm, repl_tool, search_tool

    print("=== Tool smoke tests ===")
    print(repl_tool.invoke(
    "print('testing the python tool by a simple maths operation -->',3-7)"
))

    print("testing the google serving tools -->")
    print(serper_tool.invoke(
    "did pm Modi attended the g7 meeting in france?"
))

    print("\n=== Python-only agent ===")

    # Step 3 here
    agent_executer_one=AgentExecutor(
    agent=react_agent,
    tools=[repl_tool],
    verbose=True
)

    user_input = (
        "If $ 450 amounts to $ 630 in 6 years, what will it amount to in 2 years "
        "at the same interest rate?"
    )

    response=agent_executer_one.invoke(
        {"input":user_input}
    )

    print(response["output"])


    print("\n=== Two-tool search agent ===")

    # Step 4 here
    agent_executer_two=AgentExecutor(
    agent=react_agent,
    tools=[serper_tool,repl_tool],
    handle_parsing_errors=True,
    verbose=True
)

    user_input="Find out what is the maximum speed of Vande Bharat train , and then calculate in how much time that train will travel to mumbai from delhi at that maximum speed ?"

    response_two =agent_executer_two.invoke(
        {"input":user_input}
    )

    print(response_two["output"])



if __name__ == "__main__":
    main()

