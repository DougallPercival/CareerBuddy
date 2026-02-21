-- ============================================
-- Raw table for StatsCan Employment Income extract
-- Schema: raw
-- Table: raw.ext_src_stc_income
-- ============================================

CREATE TABLE IF NOT EXISTS raw.src_ext_stc_income (

    -- source columns (unaltered from CSV)
    "refDate" TEXT,
    "geo" TEXT,
    "DGUID" TEXT,
    "workActivityRefYear" TEXT,
    "age" TEXT,
    "gender" TEXT,
    "statistics" TEXT,
    "coordinate" TEXT,
    "totEmpIncStat" TEXT,
    "withEmpInc" TEXT,
    "medEmpInc" TEXT,
    "avgEmpInc" TEXT,
    "withWageSalaryComm" TEXT,
    "medWageSalaryComm" TEXT,
    "avgWageSalaryComm" TEXT,
    "code" TEXT,

    -- Metadata columns
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source_file TEXT,
    load_batch_id UUID,
    row_number BIGINT,

    -- surrogate key
    raw_id BIGSERIAL PRIMARY KEY
);
