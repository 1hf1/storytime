from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from typing import Dict, Any
import uuid
import os
import dotenv
from .tester_tools import create_tester_tools

backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(backend_dir, '.env')
dotenv.load_dotenv(env_path)

from .prompts import tester_agent_system_prompt
from ...evaluations.evaluation import EvaluationReport
class TesterAgent:
    def __init__(self, story: StoryStructure, model: str = "gpt-4o-mini", tools = []):
        self.model = model
        self.evaluation_report = EvaluationReport(story)
        self.tools = create_tester_tools(self.evaluation_report) + tools
        self.system_prompt = tester_agent_system_prompt
        self.checkpointer = InMemorySaver()
        self.thread_id = str(uuid.uuid4())
        self.agent = create_agent(
            model=model,
            tools=self.tools,
            system_prompt=self.system_prompt,
            checkpointer=self.checkpointer
        )
        self.story = story
    def test_story(self):
        import json
        story_json_str = json.dumps(self.story.to_json(), indent=2)
        response = self.agent.invoke({
            "messages": [{
                "role": "user", 
                "content": f"Test the story and save the evaluation report. The story is:\n\n{story_json_str}"
            }]
        }, config={"configurable": {"thread_id": self.thread_id}})
        return response
