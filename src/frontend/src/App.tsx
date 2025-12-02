import { useState } from 'react';
import { HomePage } from './components/HomePage';
import { StoryView } from './components/StoryView';
import { CreateStory, StoryData } from './components/CreateStory';

type View = 'home' | 'create' | 'view';

function App() {
  const [currentView, setCurrentView] = useState<View>('home');
  const [currentStory, setCurrentStory] = useState<StoryData | null>(null);
  const [loading, setLoading] = useState(false);

  const handleCreateStory = () => {
    setCurrentView('create');
  };

  const handleBack = () => {
    setCurrentView('home');
    setCurrentStory(null);
  };

  const handleStoryCreated = (storyData: StoryData) => {
    setCurrentStory(storyData);
    setCurrentView('view');
  };

  const handleStorySelect = async (filename: string) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/stories/${filename}`);
      const data = await response.json();
      setCurrentStory(data);
      setCurrentView('view');
    } catch (error) {
      console.error('Error loading story:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#f5f3eb] flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-4 border-forest-600 border-t-transparent"></div>
      </div>
    );
  }

  return (
    <>
      {currentView === 'view' && currentStory ? (
        <StoryView story={currentStory} onBack={handleBack} />
      ) : currentView === 'create' ? (
        <CreateStory onBack={handleBack} onStoryCreated={handleStoryCreated} />
      ) : (
        <HomePage onCreateStory={handleCreateStory} onStorySelect={handleStorySelect} />
      )}
    </>
  );
}

export default App;
