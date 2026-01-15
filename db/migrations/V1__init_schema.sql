-- V1: базовая схема для прогнозирования финансового состояния

CREATE TABLE IF NOT EXISTS companies (
  id              BIGSERIAL PRIMARY KEY,
  inn             VARCHAR(12) NOT NULL UNIQUE,
  name            TEXT,
  created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reporting_periods (
  id              BIGSERIAL PRIMARY KEY,
  year            INT NOT NULL,
  quarter         INT, -- NULL если годовой отчёт
  UNIQUE(year, quarter)
);

-- 35 входных признаков (как в твоём GUI: 35 полей)
CREATE TABLE IF NOT EXISTS financial_features (
  id                  BIGSERIAL PRIMARY KEY,
  company_id           BIGINT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
  period_id            BIGINT NOT NULL REFERENCES reporting_periods(id),
  features_json        JSONB NOT NULL,        -- {"f1":..., "f35":...}
  created_at           TIMESTAMP NOT NULL DEFAULT NOW(),
  UNIQUE(company_id, period_id)
);

-- 11 регрессионных метрик + 1 классификация (риск)
CREATE TABLE IF NOT EXISTS predictions (
  id                  BIGSERIAL PRIMARY KEY,
  company_id           BIGINT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
  period_id            BIGINT NOT NULL REFERENCES reporting_periods(id),
  model_version        TEXT NOT NULL,         -- "1.0.1"
  reg_outputs_json     JSONB NOT NULL,        -- {"y1":..., "y11":...}
  risk_score           DOUBLE PRECISION NOT NULL, -- 0..1
  explanation_json     JSONB,                 -- пока NULL в v1
  created_at           TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_log (
  id                  BIGSERIAL PRIMARY KEY,
  event_time          TIMESTAMP NOT NULL DEFAULT NOW(),
  actor               TEXT NOT NULL,          -- "system" / user login
  action              TEXT NOT NULL,          -- "PREDICT", "IMPORT", ...
  entity              TEXT NOT NULL,          -- "predictions", ...
  entity_id           BIGINT,
  payload             JSONB
);

CREATE INDEX IF NOT EXISTS idx_features_company_period ON financial_features(company_id, period_id);
CREATE INDEX IF NOT EXISTS idx_predictions_company_period ON predictions(company_id, period_id);
