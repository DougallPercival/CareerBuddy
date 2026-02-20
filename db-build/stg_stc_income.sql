-- ============================================
-- Staging table for cleaned StatsCan Employment Income
-- Schema: staging
-- Table: staging.stc_income
-- ============================================

CREATE TABLE IF NOT EXISTS staging.stc_income (

    -- Primary key (optional)
    stc_income_id BIGSERIAL PRIMARY KEY,

    -- Source / cleaned columns
    refDate BIGINT,
    geo TEXT,
    DGUID TEXT,
    workActivityRefYear TEXT,
    age TEXT,
    gender TEXT,
    statistics TEXT,
    coordinate TEXT,
    totEmpIncStat BIGINT,
    withEmpInc BIGINT,
    medEmpInc BIGINT,
    avgEmpInc BIGINT,
    withWageSalaryComm BIGINT,
    medWageSalaryComm BIGINT,
    avgWageSalaryComm BIGINT,
    code TEXT,

    -- Metadata
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    load_batch_id UUID
);
