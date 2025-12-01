from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.stories.story_structure import StoryStructure
from backend.agents.newsAgent.newsAgent import NewsAgent
from backend.agents.newsAgent.prompts import news_agent_writing_action_prompt
import asyncio
import os
import json

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/generate-story")
async def generate_story(topic: str):
    try:
        story = StoryStructure(topic)
        agent = NewsAgent(story)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: agent.invoke({
                "messages": [{
                    "role": "user", 
                    "content": news_agent_writing_action_prompt.format(topic=topic)
                }]
            })
        )
        result = agent.story.to_json()
        if not result.get("title"):
            raise HTTPException(status_code=500, detail="Story generation completed but title is missing")
        return result
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Error generating story: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error generating story: {str(e)}")

@app.get("/stories")
async def list_stories():
    """List all saved stories from JSON storage."""
    try:
        storage_dir = "backend/stories/json_storage"
        stories = []
        if os.path.exists(storage_dir):
            for filename in os.listdir(storage_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(storage_dir, filename), 'r') as f:
                        data = json.load(f)
                    stat = os.stat(os.path.join(storage_dir, filename))
                    stories.append({
                        "filename": filename,
                        "title": data.get("title", "Untitled"),
                        "modified_at": stat.st_mtime,
                        "thumbnail": data.get("segments", [{}])[0].get("images", [None])[0] if data.get("segments") else None
                    })
        stories.sort(key=lambda x: x["modified_at"], reverse=True)
        return stories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stories/{filename}")
async def get_story(filename: str):
    """Get a specific story by filename."""
    try:
        filepath = os.path.join("backend/stories/json_storage", filename)
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Story not found")
        with open(filepath, 'r') as f:
            return json.load(f)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))