from ..agents.newsAgent.newsAgent import NewsAgent
from ..stories.story_structure import StoryStructure
from ..agents.testerAgent.testerAgent import TesterAgent
import time

def run_simulation_testing(n_topics: int = 10):
    story_generator_prompt = "Randomly select a news or historical topic that is real and for which there are valid sources and write a story about it. No need to generate images for these stories."
    evaluation_reports = []
    
    for i in range(n_topics):
        story_location = f"simulation_story_{i}_{int(time.time())}"
        story = StoryStructure(story_location)
        
        news_agent = NewsAgent(story)
        
        response = news_agent.invoke({
            "messages": [{
                "role": "user", 
                "content": story_generator_prompt
            }]
        })
        
        tester = TesterAgent(story)
        tester.test_story()
        
        evaluation_reports.append(tester.evaluation_report.to_json())
        story.delete()
    
    return evaluation_reports
