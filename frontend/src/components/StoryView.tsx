import { ArrowLeft, BookOpen } from 'lucide-react';
import { StoryData } from './CreateStory';

type StoryViewProps = {
  story: StoryData;
  onBack: () => void;
};

export function StoryView({ story, onBack }: StoryViewProps) {
  return (
    <div className="min-h-screen bg-[#f5f3eb]">
      <div className="container mx-auto px-8 py-12 max-w-5xl">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-forest-700 hover:text-forest-900 transition-colors mb-12 group"
        >
          <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
          <span className="font-semibold text-lg">Back to Stories</span>
        </button>

        <article className="bg-white rounded-[3rem] shadow-xl overflow-hidden">
          <div className="bg-forest-800 px-12 py-16 text-white">
            <div className="flex items-center gap-3 mb-6">
              <BookOpen className="w-10 h-10" />
              <span className="text-forest-200 font-semibold text-lg">StoryTime</span>
            </div>
            <h1 className="text-6xl font-display font-bold leading-tight">{story.title}</h1>
          </div>

          <div className="p-12 md:p-16">
            {story.segments.map((segment, segmentIndex) => (
              <section key={segmentIndex} className="mb-20 last:mb-0">
                <h2 className="text-4xl font-display font-bold text-forest-900 mb-8">
                  {segment.title}
                </h2>

                {segment.images.length > 0 && (
                  <div className={`mb-8 ${segment.images.length > 1 ? 'grid grid-cols-2 gap-6' : ''}`}>
                    {segment.images.map((imageUrl, imageIndex) => (
                      <div
                        key={imageIndex}
                        className="rounded-[2rem] overflow-hidden shadow-lg"
                      >
                        <img
                          src={imageUrl}
                          alt={segment.title}
                          className="w-full h-auto object-cover"
                        />
                      </div>
                    ))}
                  </div>
                )}

                <div className="prose prose-lg max-w-none">
                  {segment.text.split('\n\n').map((paragraph, idx) => (
                    <p key={idx} className="text-forest-900 leading-relaxed mb-6 text-xl">
                      {paragraph}
                    </p>
                  ))}
                </div>

                {segmentIndex < story.segments.length - 1 && (
                  <div className="mt-12 flex justify-center">
                    <div className="w-24 h-1 bg-gradient-to-r from-transparent via-forest-400 to-transparent"></div>
                  </div>
                )}
              </section>
            ))}
          </div>
        </article>
      </div>
    </div>
  );
}
