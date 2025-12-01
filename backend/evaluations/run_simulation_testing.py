from backend.agents.newsAgent.newsAgent import NewsAgent
from backend.stories.story_structure import StoryStructure
from backend.agents.testerAgent.testerAgent import TesterAgent
import time

def run_simulation_testing(n_topics: int = 10):
    story_generator_prompt = "Randomly select a news or historical topic that is real and for which there are valid sources and write a story about it. No need to generate images for these stories."
    evaluation_reports = []
    
    for i in range(n_topics):
        # Create a new story with a unique location
        story_location = f"simulation_story_{i}_{int(time.time())}"
        story = StoryStructure(story_location)
        
        # Create the news agent with the story object
        news_agent = NewsAgent(story)
        
        # Generate the story
        response = news_agent.invoke({
            "messages": [{
                "role": "user", 
                "content": story_generator_prompt
            }]
        })
        
        # Test the story (story is already updated by the agent)
        tester = TesterAgent(story)
        tester.test_story()
        
        # Collect the evaluation report
        evaluation_reports.append(tester.evaluation_report.to_json())
        
        # Optional: delete the story file if you don't want to keep it
        story.delete()
    
    return evaluation_reports
