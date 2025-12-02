from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from typing import Dict, Any
import uuid
import os
import dotenv
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(backend_dir, '.env')
dotenv.load_dotenv(env_path)

from .prompts import news_agent_system_prompt
from .story_tools_interface import create_story_tools
from ...stories.story_structure import StoryStructure

class NewsAgent:
    def __init__(self, story: StoryStructure, model: str = "gpt-4o-mini", tools = []):
        self.story = story
        self.model = model
        self.system_prompt = news_agent_system_prompt
        self.tools = create_story_tools(story) + tools
        self.checkpointer = InMemorySaver()
        self.thread_id = str(uuid.uuid4())
        self.agent = create_agent( 
            model=model,
            tools=self.tools,
            system_prompt=self.system_prompt,
            checkpointer=self.checkpointer
        )
    
    def invoke(self, input: Dict[str, Any]):
        response = self.agent.invoke(input, config={"configurable": {"thread_id": self.thread_id}})
        return response
