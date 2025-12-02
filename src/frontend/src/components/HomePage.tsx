import { Plus } from 'lucide-react';
import { useState, useEffect } from 'react';

type HomePageProps = {
  onCreateStory: () => void;
  onStorySelect: (filename: string) => void;
};

type Story = {
  filename: string;
  title: string;
  modified_at: number;
  thumbnail?: string;
};

export function HomePage({ onCreateStory, onStorySelect }: HomePageProps) {
  const [stories, setStories] = useState<Story[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/stories')
      .then(res => res.json())
      .then(data => setStories(data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-[#f5f3eb]">
      <div className="container mx-auto px-8 py-12 max-w-7xl">
        <div className="flex items-center justify-between mb-16">
          <h1 className="text-7xl font-display font-bold text-forest-800">
            Stories
          </h1>
          <button
            onClick={onCreateStory}
            className="flex items-center gap-3 px-8 py-4 bg-forest-700 text-white rounded-full font-bold text-lg hover:bg-forest-800 transition-all shadow-lg hover:shadow-xl hover:scale-105"
          >
            <Plus className="w-6 h-6" />
            Create Story
          </button>
        </div>

        <div className="mb-16">
          {loading ? (
            <div className="flex justify-center py-20">
              <div className="animate-spin rounded-full h-16 w-16 border-4 border-forest-600 border-t-transparent"></div>
            </div>
          ) : stories.length === 0 ? (
            <div className="bg-white rounded-[3rem] shadow-xl p-16 text-center">
              <p className="text-xl text-forest-700">No stories yet. Create your first one!</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {stories.map((story) => (
                <button
                  key={story.filename}
                  onClick={() => onStorySelect(story.filename)}
                  className="bg-white rounded-[2rem] shadow-lg hover:shadow-2xl transition-all overflow-hidden text-left group hover:scale-105"
                >
                  {story.thumbnail && (
                    <div className="w-full h-48 overflow-hidden">
                      <img src={story.thumbnail} alt={story.title} className="w-full h-full object-cover" />
                    </div>
                  )}
                  <div className="p-6">
                    <h3 className="text-2xl font-display font-bold text-forest-900 group-hover:text-forest-600">
                      {story.title}
                    </h3>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
