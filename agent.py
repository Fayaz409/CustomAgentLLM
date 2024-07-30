import os 
import yaml
import json
import requests
from termcolor import colored
from prompts import planning_agent_prompt, integration_agent_prompt
from search import WebSearcher

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        for key, value in config.items():
            os.environ[key] = value

class Agent:
    """
    Agent class to manage the interaction between a user query and the WebSearcher tool.

    Methods:
        __init__(model: str, tool: class, temperature: int, max_tokens: int, planning_agent_prompt: str, integration_agent_prompt: str, verbose: bool): Initializes the Agent instance.
        run_planning_agent(query: str, plan: str, outputs: str, feedback: str) -> str: Runs the planning agent to create a plan based on the query.
        run_integration_agent(query: str, plan: str, outputs: str) -> str: Runs the integration agent to process the plan and outputs.
        check_response(response: str, query: str) -> bool: Checks if the response meets the query requirements.
        execute(iterations: int): Executes the entire query planning, search, and response integration workflow.
    """

    def __init__(self, model, tool, temperature=0, max_tokens=1000, planning_agent_prompt=None, integration_agent_prompt=None, verbose=False):
        load_config('config.yaml')
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.url = 'https://api.openai.com/v1/chat/completions'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.tool = tool
        self.tool_specs = tool.__doc__
        self.planning_agent_prompt = planning_agent_prompt
        self.integration_agent_prompt = integration_agent_prompt
        self.model = model
        self.verbose = verbose
    
    def run_planning_agent(self, query, plan=None, outputs=None, feedback=None):
        """
        Generates a plan using the planning agent based on the user query.
        """
        system_prompt = self.planning_agent_prompt.format(
            outputs=outputs,
            plan=plan,
            feedback=feedback,
            tool_specs=self.tool_specs
        )

        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": query},
                         {"role": "system", "content": system_prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        json_data = json.dumps(data)
        response = requests.post(self.url, headers=self.headers, data=json_data, timeout=180)
        response_dict = response.json()
        content = response_dict['choices'][0]['message']['content']
        if self.verbose:
            print(colored(f"Planning Agent: {content}", 'green'))

        return content
    
    def run_integration_agent(self, query, plan, outputs):
        """
        Processes the plan and outputs using the integration agent.
        """
        system_prompt = self.integration_agent_prompt.format(
            outputs=outputs,
            plan=plan
        )

        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": query},
                         {"role": "system", "content": system_prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        json_data = json.dumps(data)
        response = requests.post(self.url, headers=self.headers, data=json_data, timeout=180)
        response_dict = response.json()
        content = response_dict['choices'][0]['message']['content']
        if self.verbose:
            print(colored(f"Integration Agent: {content}", 'blue'))

        return content
    
    def check_response(self, response, query):
        """
        Checks if the response meets the requirements of the query.
        """
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "response_checker",
                    "description": "Check if the response meets the requirements",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "meets_requirements": {
                                "type": "string",
                                "description": """Check if the response meets the requirements of the query based on the following:
                                1. The response should be relevant to the query.
                                2. The response should be coherent and well-structured with citations.
                                3. The response should be comprehensive and address the query in its entirety.
                                Return 'yes' if the response meets the requirements and 'no' otherwise.
                                """
                            },
                        },
                        "required": ["meets_requirements"]
                    }
                }
            }
        ]

        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": f"Response: {response} \n Query: {query}"}],
            "temperature": 0,
            "tools": tools,
            "tool_choice": "required"
        }

        json_data = json.dumps(data)
        response = requests.post(self.url, headers=self.headers, data=json_data, timeout=180)
        response_dict = response.json()

        tool_calls = response_dict['choices'][0]['message']['tool_calls'][0]
        arguments_json = json.loads(tool_calls['function']['arguments'])
        response_check = arguments_json['meets_requirements']

        return response_check == 'yes'

    def execute(self, iterations=5):
        """
        Executes the workflow: planning, searching, and integrating the response.
        """
        query = input("Enter your query: ")
        tool = self.tool(model=self.model, verbose=self.verbose)
        meets_requirements = False
        plan = None
        outputs = None
        response = None
        links = None
        iterations = 0

        while not meets_requirements and iterations < 5:
            iterations += 1  
            plan = self.run_planning_agent(query, plan=plan, outputs=outputs, feedback=response)
            results_dict = tool.use_tool(plan=plan, query=query)
            outputs = "\n".join(results_dict.values())
            links = "\n".join(results_dict.keys())
            response = self.run_integration_agent(query, plan, outputs)
            meets_requirements = self.check_response(response, query)

        print(colored(f"Final Response: {response}", 'cyan'))
        print(colored(f"Links: {links}", 'magenta'))

if __name__ == '__main__':
    agent = Agent(
        model="gpt-3.5-turbo",
        tool=WebSearcher, 
        planning_agent_prompt=planning_agent_prompt, 
        integration_agent_prompt=integration_agent_prompt,
        verbose=True
    )
    agent.execute()