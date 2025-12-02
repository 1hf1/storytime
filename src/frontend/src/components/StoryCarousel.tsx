import { ChevronLeft, ChevronRight } from 'lucide-react';
import { useState, useEffect } from 'react';

type CarouselStory = {
  id: string;
  title: string;
  slug: string;
  imageUrl?: string;
};

type StoryCarouselProps = {
  stories: CarouselStory[];
  onStoryClick: (slug: string) => void;
};

export function StoryCarousel({ stories, onStoryClick }: StoryCarouselProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const storiesPerPage = 3;
  const maxIndex = Math.max(0, stories.length - storiesPerPage);

  useEffect(() => {
    if (currentIndex > maxIndex) {
      setCurrentIndex(maxIndex);
    }
  }, [stories.length, maxIndex, currentIndex]);

  useEffect(() => {
    if (stories.length === 0) return;

    const interval = setInterval(() => {
      setCurrentIndex((prev) => {
        const next = prev + 1;
        return next > maxIndex ? 0 : next;
      });
    }, 5000);

    return () => clearInterval(interval);
  }, [maxIndex, stories.length]);

  const goToPrevious = () => {
    setCurrentIndex((prev) => {
      const newIndex = prev - 1;
      return newIndex < 0 ? maxIndex : newIndex;
    });
  };

  const goToNext = () => {
    setCurrentIndex((prev) => {
      const newIndex = prev + 1;
      return newIndex > maxIndex ? 0 : newIndex;
    });
  };

  const visibleStories = stories.slice(currentIndex, currentIndex + storiesPerPage);

  if (stories.length === 0) {
    return (
      <div className="text-center py-12 text-slate-500">
        <p className="text-lg">No stories available yet. Be the first to create one!</p>
      </div>
    );
  }

  return (
    <div className="relative">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {visibleStories.map((story, idx) => (
          <button
            key={story.id}
            onClick={() => onStoryClick(story.slug)}
            className="group bg-white rounded-[2.5rem] shadow-lg hover:shadow-2xl transition-all duration-500 overflow-hidden hover:scale-[1.02]"
          >
            <div className="aspect-[4/3] overflow-hidden bg-forest-50 relative">
              {story.imageUrl ? (
                <img
                  src={story.imageUrl}
                  alt={story.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <div className="text-6xl">📖</div>
                </div>
              )}
            </div>
            <div className="p-6 text-center">
              <h3 className="text-xl font-bold text-black line-clamp-2">
                {story.title}
              </h3>
            </div>
          </button>
        ))}
      </div>

      <div className="flex justify-center gap-3 mt-10">
        <button
          onClick={goToPrevious}
          className="p-2 rounded-full hover:bg-forest-100 transition-all"
          aria-label="Previous stories"
        >
          <ChevronLeft className="w-6 h-6 text-forest-700" />
        </button>

        {Array.from({ length: maxIndex + 1 }).map((_, idx) => (
          <button
            key={idx}
            onClick={() => setCurrentIndex(idx)}
            className={`h-3 rounded-full transition-all ${
              idx === currentIndex ? 'w-8 bg-forest-600' : 'w-3 bg-forest-300 hover:bg-forest-400'
            }`}
            aria-label={`Go to page ${idx + 1}`}
          />
        ))}

        <button
          onClick={goToNext}
          className="p-2 rounded-full hover:bg-forest-100 transition-all"
          aria-label="Next stories"
        >
          <ChevronRight className="w-6 h-6 text-forest-700" />
        </button>
      </div>
    </div>
  );
}
