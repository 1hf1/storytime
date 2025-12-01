"""Tool agent interface for tester agent to interact with evaluation reports. Written by Cursor (Claude) using previously written code defining the tester agent, the evaluation report class. and the news agent tools file."""

from langchain.tools import tool
from backend.evaluations.evaluation import EvaluationReport
from backend.stories.story_structure import StoryStructure
from backend.agents.newsAgent.newsAgent import NewsAgent
import os

def create_tester_tools(evaluation_report: EvaluationReport = None):
    """Create LangChain tools for the tester agent to generate stories and create evaluation reports."""
    
    current_evaluation = evaluation_report
    current_story = None
    
    @tool
    def generate_story(topic: str) -> str:
        """Generate a story about a given topic using the NewsAgent.
        
        Args:
            topic: The topic to generate a story about
            
        Returns:
            The full story as a JSON string including title, segments, images, research document, and citations
        """
        nonlocal current_story, current_evaluation
        try:
            # Create a new story structure
            story = StoryStructure()
            
            # Create a news agent with the story
            news_agent = NewsAgent(story=story)
            
            # Generate the story
            from backend.agents.newsAgent.prompts import news_agent_writing_action_prompt
            prompt = news_agent_writing_action_prompt.format(topic=topic)
            response = news_agent.invoke({"messages": [{"role": "user", "content": prompt}]})
            
            # Store the current story for evaluation
            current_story = story
            current_evaluation = EvaluationReport(story)
            
            # Return the full story JSON
            import json
            story_data = story.to_json()
            return f"Story generated successfully:\n{json.dumps(story_data, indent=2)}"
        except Exception as e:
            return f"Error generating story: {str(e)}"
    
    @tool
    def perplexity_search(query: str) -> str:
        """Search for information using Perplexity web search for fact-checking.
        
        Args:
            query: The search query to look up information about
            
        Returns:
            Formatted search results with titles, URLs, and snippets
        """
        from perplexity import Perplexity
        
        try:
            perplexity_client = Perplexity(api_key=os.getenv("PERPLEXITY_API_KEY"))
            search = perplexity_client.search.create(
                query=query,
                max_results=5,
                max_tokens_per_page=1024
            )
            
            results = []
            for result in search.results:
                result_text = f"Title: {result.title}\nURL: {result.url}\nSnippet: {getattr(result, 'snippet', '')}"
                results.append(result_text)
            
            formatted_results = "\n\n".join(results)
            return f"Search completed. Found {len(results)} results.\n\n{formatted_results}"
        except Exception as e:
            return f"Error searching Perplexity: {str(e)}"
    
    @tool
    def get_current_evaluation_status() -> str:
        """Get the current status of the evaluation report.
        
        Returns:
            Summary of current evaluation metrics and report status
        """
        nonlocal current_evaluation
        if current_evaluation is None:
            return "No evaluation report exists. Please generate a story first."
        
        import json
        status = {
            "accuracy_proportion": current_evaluation.accuracy_proportion,
            "citations_proportion": current_evaluation.citations_proportion,
            "report": current_evaluation.report
        }
        return json.dumps(status, indent=2)
    
    @tool
    def update_evaluation_report(accuracy_proportion: float = None, citations_proportion: float = None, accuracy_report: str = None, citations_report: str = None) -> str:
        """Update the evaluation report with accuracy and citations metrics and details.
        
        Args:
            accuracy_proportion: A float between 0 and 1 representing the proportion of accurate content (optional)
            citations_proportion: A float between 0 and 1 representing the proportion of facts supported by citations (optional)
            accuracy_report: Detailed text describing accuracy findings (optional)
            citations_report: Detailed text describing citations findings (optional)
            
        Returns:
            Confirmation message
        """
        nonlocal current_evaluation
        if current_evaluation is None:
            return "No evaluation report exists. Please generate a story first."
        
        # Validate proportions
        if accuracy_proportion is not None and not 0 <= accuracy_proportion <= 1:
            return "Accuracy proportion must be between 0 and 1"
        
        if citations_proportion is not None and not 0 <= citations_proportion <= 1:
            return "Citations proportion must be between 0 and 1"
        
        # Use the update_report method from EvaluationReport class
        current_evaluation.update_report(
            accuracy_proportion=accuracy_proportion,
            citations_proportion=citations_proportion,
            accuracy_report=accuracy_report,
            citations_report=citations_report
        )
        
        # Build confirmation message
        updates = []
        if accuracy_proportion is not None:
            updates.append(f"accuracy proportion to {accuracy_proportion}")
        if citations_proportion is not None:
            updates.append(f"citations proportion to {citations_proportion}")
        if accuracy_report is not None:
            updates.append("accuracy report details")
        if citations_report is not None:
            updates.append("citations report details")
        
        if not updates:
            return "No updates provided"
        
        return f"Updated evaluation report: {', '.join(updates)}"
    
    @tool
    def calculate_evaluation_metrics(total, num_correct):
        """Very simple tools to calculate proportions of accuracy and citations in the current evaluation report. Just provide
        the total number of facts in the story and the number of facts that are accurate or supported by citations and 
        the function will calculate the proportions.
        """
        proportion = num_correct / total
        return "Proportion: " + str(proportion)
    @tool
    def save_evaluation_report(report_name: str) -> str:
        """Save the current evaluation report to disk.
        
        Args:
            report_name: The name to save the report under (without .json extension)
            
        Returns:
            Confirmation message with save location
        """
        nonlocal current_evaluation
        if current_evaluation is None:
            return "No evaluation report exists. Please generate a story first."
        
        try:
            current_evaluation.save_report(report_name)
            return f"Evaluation report saved successfully as '{report_name}.json'"
        except Exception as e:
            return f"Error saving evaluation report: {str(e)}"
    
    return [
        generate_story,
        perplexity_search,
        get_current_evaluation_status,
        update_evaluation_report,
        save_evaluation_report,
        calculate_evaluation_metrics
    ]
