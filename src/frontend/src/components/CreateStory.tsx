import { useState } from 'react';
import { ArrowLeft, Plus, Loader2 } from 'lucide-react';

type CreateStoryProps = {
  onBack: () => void;
  onStoryCreated: (storyData: StoryData) => void;
};

export type StoryData = {
  title: string;
  research_document: string;
  segments: {
    title: string;
    text: string;
    images: string[];
  }[];
};

export function CreateStory({ onBack, onStoryCreated }: CreateStoryProps) {
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState('');

  const handleGenerate = async () => {
    if (!topic.trim()) {
      setError('Please enter a topic');
      return;
    }

    setLoading(true);
    setError(null);
    setProgress('Generating story...');

    try {
      setProgress('Contacting story generation API...');
      const response = await fetch(
        `http://localhost:8000/generate-story?topic=${encodeURIComponent(topic)}`,
        {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
          },
          signal: AbortSignal.timeout(300000),
        }
      );

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }

      setProgress('Processing story data...');
      const storyData: StoryData = await response.json();

      setProgress('Story created successfully!');
      setTimeout(() => {
        onStoryCreated(storyData);
      }, 500);
    } catch (err) {
      console.error('Error generating story:', err);
      if (err instanceof Error) {
        if (err.name === 'TimeoutError') {
          setError('Story generation timed out. Please try again with a simpler topic.');
        } else if (err.message.includes('Failed to fetch') || err.message.includes('ECONNREFUSED')) {
          setError('Could not connect to the story generation API. Please ensure it is running on http://localhost:8000');
        } else {
          setError(err.message);
        }
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
      setLoading(false);
      setProgress('');
    }
  };

  return (
    <div className="min-h-screen bg-[#f5f3eb]">
      <div className="container mx-auto px-8 py-12 max-w-4xl">
        <button
          onClick={onBack}
          disabled={loading}
          className="flex items-center gap-2 text-forest-700 hover:text-forest-900 transition-colors mb-12 group disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
          <span className="font-semibold text-lg">Back to Stories</span>
        </button>

        <div className="bg-white rounded-[3rem] shadow-xl p-12">
          <div className="flex items-center gap-4 mb-8">
            <Plus className="w-10 h-10 text-forest-700" />
            <h1 className="text-5xl font-display font-bold text-forest-900">
              Create New Story
            </h1>
          </div>

          <div className="space-y-6">
            <div>
              <label
                htmlFor="topic"
                className="block text-xl font-semibold text-forest-900 mb-3"
              >
                Story Topic
              </label>
              <input
                id="topic"
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="Enter a topic for your story..."
                disabled={loading}
                className="w-full px-6 py-4 text-lg rounded-3xl bg-[#f5f3eb] border-2 border-forest-200 focus:border-forest-500 focus:outline-none focus:ring-4 focus:ring-forest-100 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !loading) {
                    handleGenerate();
                  }
                }}
              />
              <p className="mt-2 text-forest-600 text-sm">
                Examples: "Trump Tariffs", "Tesla Stock Adventure", "Climate Change Updates"
              </p>
            </div>

            {error && (
              <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-4">
                <p className="text-red-700 font-medium">{error}</p>
              </div>
            )}

            {loading && progress && (
              <div className="bg-forest-50 border-2 border-forest-200 rounded-2xl p-4">
                <div className="flex items-center gap-3">
                  <Loader2 className="w-5 h-5 text-forest-700 animate-spin" />
                  <p className="text-forest-800 font-medium">{progress}</p>
                </div>
                <p className="text-forest-600 text-sm mt-2">
                  This may take 30 seconds to 5 minutes depending on the complexity...
                </p>
              </div>
            )}

            <button
              onClick={handleGenerate}
              disabled={loading || !topic.trim()}
              className="w-full py-5 bg-forest-700 text-white rounded-full font-bold text-lg hover:bg-forest-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-3">
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Generating Story...
                </span>
              ) : (
                'Generate Story'
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
