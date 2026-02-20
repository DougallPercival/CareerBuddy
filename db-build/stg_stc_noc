-- ============================================
-- Staging table for cleaned StatsCan NOC data
-- Schema: staging
-- Table: staging.stc_noc
-- ============================================

CREATE TABLE IF NOT EXISTS staging.stc_noc (

    -- Primary key (optional)
    stc_noc_id BIGSERIAL PRIMARY KEY,

    -- Cleaned NOC columns
    level TEXT,
    hierarchy TEXT,
    code TEXT,
    classTitle TEXT,
    classDefinition TEXT,

    -- Optional metadata for batch tracking
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    load_batch_id UUID
);
