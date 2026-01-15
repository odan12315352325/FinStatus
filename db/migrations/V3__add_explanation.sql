
ALTER TABLE predictions
  ADD COLUMN IF NOT EXISTS explanation_json JSONB;
