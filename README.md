## Project: Web-Based Query Response Agent

This project is a web-based query response agent designed to automate the process of generating search queries, retrieving web content, and synthesizing responses to user queries. The system leverages OpenAI's language model capabilities to create an interactive agent that collaborates with specialized tools to deliver comprehensive and relevant responses to user inputs.

### Project Structure

- **agent.py**: The main script for running the agent. It handles the interaction between the user query and the web searcher tool.
- **websearch.py**: Contains the `WebSearcher` class which is responsible for generating search queries, fetching search results, and scraping web content.
- **prompts.py**: Contains the prompts used for the planning and integration agents.
- **requirements.txt**: Lists the required Python packages.
- **config.yaml**: Configuration file to store API keys and other necessary configurations.

### Setup Instructions

1. **Clone the repository:**

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install required Python packages:**

   Make sure you have Python installed. You can install the required packages using pip:

   ```sh
   pip install -r requirements.txt
   ```

3. **Set up configuration:**

   Rename the `.yaml` file to `config.yaml` and replace the placeholders with your actual API keys.

   ```yaml
   OPENAI_API_KEY: "Your_OPENAI_API_KEY"
   SERPER_DEV_API_KEY: "Your_SERPER_DEV_API_KEY"
   ```

### How to Use

To run the agent, simply execute the following command:

```sh
python agent.py
```

Follow the on-screen instructions to input your query. The agent will go through a series of steps to generate search queries, fetch relevant results, scrape web content, and synthesize a comprehensive response to your query.

### Agent Workflow

1. **Query Input**: You provide a query to the agent.
2. **Planning Agent**: The planning agent analyzes the query and devises a strategy.
3. **Web Searcher Tool**: Based on the plan, the web searcher tool generates search queries, fetches search results, and scrapes relevant web content.
4. **Integration Agent**: The integration agent synthesizes the retrieved content into a coherent response.
5. **Response Check**: The agent checks if the response meets the query requirements. If not, the process iterates until a satisfactory response is generated.

### Example

```sh
Enter your query: What are the benefits of using AI in healthcare?
```

The agent will generate a detailed response by searching the web, retrieving relevant content, and integrating the information into a comprehensive answer.

### Additional Resources

If you want to understand the code better, please visit the following GitHub repository and YouTube video by John Adeojo, from whom this project has taken inspiration:

- GitHub: [John Adeojo's Custom Agent Tutorial](https://github.com/john-adeojo/custom_agent_tutorial/tree/main)
- YouTube: [Custom Agent Tutorial Video](https://www.youtube.com/watch?v=CV1YgIWepoI&t=1728s)

---

Follow these instructions and resources to get started with the web-based query response agent and understand the underlying code.
