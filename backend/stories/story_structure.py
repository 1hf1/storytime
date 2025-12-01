import json
import os

story_storage_dir = "stories/json_storage"

class StoryStructure:
    def __init__(self, location: str):
        self.location = os.path.join(story_storage_dir, location + ".json")
        self.title = ""
        self.research_document = ""
        self.segments = []
        self.citations = []
        
    def add_segment(self, title: str, text: str = "", images: list = None, citations: list = None):
        """Add a new segment to the story."""
        segment = {
            "title": title,
            "text": text,
            "images": images or [],
        }
        self.segments.append(segment)
    
    #The following utility functions were drafted by Cursor (Claude) with clear specification on what functionality was needed.
    def find_segment_index(self, segment_title: str) -> int:
        """Find segment index by title."""
        for i, seg in enumerate(self.segments):
            if seg.get('title') == segment_title:
                return i
        return -1
    
    def write_story_section(self, segment_title: str, segment_section: str, value, replace: bool = False):
        """Write to a specific section of a segment."""
        idx = self.find_segment_index(segment_title)
        if idx == -1:
            raise ValueError(f"Segment '{segment_title}' not found")
        
        if replace:
            self.segments[idx][segment_section] = value
        else:
            if isinstance(self.segments[idx][segment_section], list):
                self.segments[idx][segment_section].extend(value if isinstance(value, list) else [value])
            else:
                self.segments[idx][segment_section] += value
    
    def write_story_title(self, title: str):
        """Set the story title."""
        self.title = title
    
    def set_research_document(self, research_text: str, replace: bool = False):
        """Set or append to the research document."""
        if replace:
            self.research_document = research_text
        else:
            self.research_document += "\n" + research_text if self.research_document else research_text
    
    def to_json(self) -> dict:
        """Return story as JSON dict."""
        return {
            "title": self.title,
            "research_document": self.research_document,
            "segments": self.segments
        }
    
    def save_to_file(self, target_path: str = None):
        """Save story to JSON file.
        
        Args:
            target_path: Optional explicit path. Defaults to the story's primary location.
        """
        os.makedirs(story_storage_dir, exist_ok=True)
        destination = target_path or self.location
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with open(destination, 'w') as f:
            json.dump(self.to_json(), f, indent=2)
    
    def load_from_file(self):
        """Load story from JSON file."""
        if os.path.exists(self.location):
            with open(self.location, 'r') as f:
                data = json.load(f)
                self.title = data.get('title', '')
                self.research_document = data.get('research_document', '')
                self.segments = data.get('segments', [])
                self.citations = data.get('citations', [])
    def save_story(self, version_name: str) -> str:
        """Save the current story to a versioned JSON file alongside the base story file."""
        if not version_name:
            raise ValueError("version_name must be provided")
        base_dir = os.path.dirname(self.location)
        base_name = os.path.splitext(os.path.basename(self.location))[0]
        version_filename = f"{base_name}-{version_name}.json"
        version_path = os.path.join(base_dir, version_filename)
        self.save_to_file(version_path)
        return version_path
    
    def delete(self):
        """Delete the story file from disk."""
        if os.path.exists(self.location):
            os.remove(self.location)
            return f"Story deleted: {self.location}"
        else:
            return f"Story file not found: {self.location}"