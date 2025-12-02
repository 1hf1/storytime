"""Tool agent interface drafted by Cursor (Claude)"""

from langchain.tools import tool
from ...stories.story_structure import StoryStructure

def create_story_tools(story: StoryStructure):
    """Create LangChain tools for interacting with a story structure."""
    story = story
    @tool
    def add_story_segment(title: str, text: str = "") -> str:
        """Add a new segment to the story. Use this when creating new sections of the story.
        
        Args:
            title: The title of the segment
            text: The text content of the segment (optional)
        """
        story.add_segment(title=title, text=text)
        return f"Added segment '{title}' to the story"
    
    @tool
    def write_segment_text(segment_title: str, text: str, replace: bool = False) -> str:
        """Write or update text in a specific story segment.
        
        Args:
            segment_title: The title of the segment to update
            text: The text to write
            replace: If True, replace existing text. If False, append to existing text.
        """
        try:
            story.write_story_section(segment_title, "text", text, replace)
            return f"Updated text in segment '{segment_title}'"
        except ValueError as e:
            return str(e)
    
    @tool
    def add_segment_image(segment_title: str, image_url: str) -> str:
        """Add an image URL to a specific story segment.
        
        Args:
            segment_title: The title of the segment
            image_url: The URL of the image to add
        """
        try:
            story.write_story_section(segment_title, "images", image_url, replace=False)
            return f"Added image to segment '{segment_title}'"
        except ValueError as e:
            return str(e)
    
    @tool
    def set_story_title(title: str) -> str:
        """Set the title of the story.
        
        Args:
            title: The story title
        """
        story.write_story_title(title)
        return f"Story title set to: {title}"
    
    @tool
    def save_story(version_name: str) -> str:
        """Persist the current story snapshot using the supplied version label."""
        if story.title == "":
            return "Story title is not set. Please set the story title first and then save the story."
        if story.segments == []:
            return "Story segments are not set. Please add segments first and then save the story."
        if story.citations == [] and story.research_document == "":
            return "Story citations or research document are not set. Please add research information first using add_research_document and then save the story."
        saved_path = story.save_story(version_name)
        return f"Story successfully saved to {saved_path}"
    
    @tool
    def get_story_json() -> str:
        """Get the current story as a JSON string. Use this to see the full story structure.
        Note: Image data is excluded to avoid token limits - images are still stored in the story object.
        """
        import json
        story_data = story.to_json()
        for segment in story_data.get('segments', []):
            if 'images' in segment and len(segment['images']) > 0:
                segment['images'] = [f"[{len(segment['images'])} images - data excluded to save tokens]"]
        return json.dumps(story_data, indent=2)
    @tool
    def add_research_document(research_text: str, replace: bool = False) -> str:
        """Add research information to the story. Use this to store research findings that inform the story.
        
        Args:
            research_text: The research information to add
            replace: If True, replace existing research. If False, append to existing research.
        """
        story.set_research_document(research_text, replace)
        return f"Research document updated. Length: {len(story.research_document)} characters"
    @tool
    def perplexity_search(query: str) -> str:
        """Search for information using Perplexity web search. Results are automatically added to the research document in
        a string format like: --- Search Query: <query> --- <formatted results> ---
        <formatted results> is a string with the title, URL, and snippet of the result.
        <query> is the search query that was used.
        --- is a separator between the search query and the formatted results.
        <formatted results> is a string with the title, URL, and snippet of the result.
        <formatted results> is a string with the title, URL, and snippet of the result.
        
        Args:
            query: The search query to look up information about
            
        Returns:
            Formatted search results with titles, URLs, and snippets
        """
        from perplexity import Perplexity
        import os
        
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
            research_entry = f"\n\n--- Search Query: {query} ---\n{formatted_results}"
            story.set_research_document(research_entry, replace=False)
            
            return f"Search completed. Found {len(results)} results. Results have been added to the research document.\n\n{formatted_results}"
        except Exception as e:
            return f"Error searching Perplexity: {str(e)}"

    @tool
    def get_story_segments() -> str:
        """Get a list of all story segment titles. Use this to see what segments have been created."""
        if not story.segments:
            return "No segments have been created yet."
        segment_titles = [seg.get('title', 'Untitled') for seg in story.segments]
        return f"Story segments: {', '.join(segment_titles)}"
    
    @tool
    def generate_and_add_image(segment_title: str, prompt: str, size: str = "1024x1024") -> str:
        """Generate an image and automatically add it to a story segment.
        
        Args:
            segment_title: The title of the segment to add the image to
            prompt: A detailed description of the image you want to generate. Make sure to mention the StoryTime style.
            size: Image size - "1024x1024", "1792x1024", or "1024x1792"
        
        Returns:
            Confirmation message that the image was added
        """
        import requests
        import os
        try:
            # Generate the image
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers={
                    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-image-1",
                    "prompt": prompt,
                    "size": size
                }
            )
            if response.status_code != 200:
                error_detail = response.text
                try:
                    error_json = response.json()
                    error_detail = error_json.get('error', {}).get('message', error_detail)
                except:
                    pass
                return f"Error generating image: HTTP {response.status_code} - {error_detail}"
            
            data = response.json()
            
            if 'data' in data and len(data['data']) > 0:
                image_data = data['data'][0]
                # Get image URL or convert base64 to data URI
                if 'url' in image_data:
                    image_url = image_data['url']
                elif 'b64_json' in image_data:
                    image_url = f"data:image/png;base64,{image_data['b64_json']}"
                else:
                    return f"Error: No image data found in response"
                
                # Add to story segment - has direct access to story via closure
                story.write_story_section(segment_title, "images", image_url, replace=False)
                return f"Generated and added image to segment '{segment_title}'"
            return f"Error: Invalid response format"
        except requests.exceptions.RequestException as e:
            return f"Error generating and adding image: Request failed - {str(e)}"
        except Exception as e:
            return f"Error generating and adding image: {str(e)}"
    
    return [
        add_story_segment,
        write_segment_text,
        add_segment_image,
        generate_and_add_image,
        set_story_title,
        save_story,
        get_story_json,
        add_research_document,
        get_story_segments,
        perplexity_search
    ]