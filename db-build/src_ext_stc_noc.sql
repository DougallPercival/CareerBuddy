-- ============================================
-- Raw table for StatsCan NOC source extract
-- Schema: raw
-- Table: raw.src_ext_stc_noc
-- ============================================

CREATE TABLE IF NOT EXISTS raw.src_ext_stc_noc (

    "Level" TEXT,
    "Hierarchical structure" TEXT,
    "Code - NOC 2021 V1.0" TEXT,
    "Class title" TEXT,
    "Class definition" TEXT,

    -- metadata columns
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source_file TEXT,
    load_batch_id UUID,
    row_number BIGINT,

    -- surrogate raw row id
    raw_id BIGSERIAL PRIMARY KEY
);
