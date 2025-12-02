/*
  # Create StoryTime Database Schema

  1. New Tables
    - `stories`
      - `id` (uuid, primary key) - Unique identifier for each story
      - `title` (text) - Main title of the story
      - `slug` (text, unique) - URL-friendly version of title for routing
      - `created_at` (timestamptz) - When the story was created
      - `updated_at` (timestamptz) - When the story was last updated
    
    - `story_segments`
      - `id` (uuid, primary key) - Unique identifier for each segment
      - `story_id` (uuid, foreign key) - References parent story
      - `title` (text) - Segment title
      - `text` (text) - Segment narrative content
      - `order_index` (integer) - Order of segment in story
      - `created_at` (timestamptz) - When segment was created
    
    - `segment_images`
      - `id` (uuid, primary key) - Unique identifier for each image
      - `segment_id` (uuid, foreign key) - References parent segment
      - `url` (text) - Image URL
      - `alt_text` (text) - Accessibility description
      - `order_index` (integer) - Order of image in segment
      - `created_at` (timestamptz) - When image was added

  2. Security
    - Enable RLS on all tables
    - Add public read policies (stories are publicly accessible)
    - Restrict write operations to authenticated users only

  3. Indexes
    - Index on stories.slug for fast lookup
    - Index on story_segments.story_id for efficient joins
    - Index on segment_images.segment_id for efficient joins
*/

-- Create stories table
CREATE TABLE IF NOT EXISTS stories (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  slug text UNIQUE NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create story_segments table
CREATE TABLE IF NOT EXISTS story_segments (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  story_id uuid NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
  title text NOT NULL,
  text text NOT NULL,
  order_index integer NOT NULL DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Create segment_images table
CREATE TABLE IF NOT EXISTS segment_images (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  segment_id uuid NOT NULL REFERENCES story_segments(id) ON DELETE CASCADE,
  url text NOT NULL,
  alt_text text DEFAULT '',
  order_index integer NOT NULL DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS stories_slug_idx ON stories(slug);
CREATE INDEX IF NOT EXISTS story_segments_story_id_idx ON story_segments(story_id);
CREATE INDEX IF NOT EXISTS segment_images_segment_id_idx ON segment_images(segment_id);

-- Enable RLS
ALTER TABLE stories ENABLE ROW LEVEL SECURITY;
ALTER TABLE story_segments ENABLE ROW LEVEL SECURITY;
ALTER TABLE segment_images ENABLE ROW LEVEL SECURITY;

-- Public read access for stories
CREATE POLICY "Anyone can read stories"
  ON stories FOR SELECT
  USING (true);

CREATE POLICY "Anyone can read story segments"
  ON story_segments FOR SELECT
  USING (true);

CREATE POLICY "Anyone can read segment images"
  ON segment_images FOR SELECT
  USING (true);

-- Authenticated users can insert stories
CREATE POLICY "Authenticated users can insert stories"
  ON stories FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Authenticated users can insert segments"
  ON story_segments FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Authenticated users can insert images"
  ON segment_images FOR INSERT
  TO authenticated
  WITH CHECK (true);

-- Authenticated users can update their content
CREATE POLICY "Authenticated users can update stories"
  ON stories FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Authenticated users can update segments"
  ON story_segments FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Authenticated users can update images"
  ON segment_images FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

-- Authenticated users can delete content
CREATE POLICY "Authenticated users can delete stories"
  ON stories FOR DELETE
  TO authenticated
  USING (true);

CREATE POLICY "Authenticated users can delete segments"
  ON story_segments FOR DELETE
  TO authenticated
  USING (true);

CREATE POLICY "Authenticated users can delete images"
  ON segment_images FOR DELETE
  TO authenticated
  USING (true);