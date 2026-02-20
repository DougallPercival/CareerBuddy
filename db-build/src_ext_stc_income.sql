-- ============================================
-- Raw table for StatsCan Employment Income extract
-- Schema: raw
-- Table: raw.ext_src_stc_income
-- ============================================

CREATE TABLE IF NOT EXISTS raw.ext_src_stc_income (

    -- source columns (unaltered from CSV)
    "REF_DATE" TEXT,
    "GEO" TEXT,
    "DGUID" TEXT,
    "Work activity during the reference year" TEXT,
    "Age" TEXT,
    "Gender" TEXT,
    "Statistics" TEXT,
    "Occupation - Minor group - National Occupational Classification" TEXT,
    "Coordinate" TEXT,
    "Total - Employment income statistics[1]" TEXT,
    "Symbol" TEXT,
    "With employment income" TEXT,
    "Symbol.1" TEXT,
    "Median employment income" TEXT,
    "Symbol.2" TEXT,
    "Average employment income" TEXT,
    "Symbol.3" TEXT,
    "With wages, salaries and commissions" TEXT,
    "Symbol.4" TEXT,
    "Median wages, salaries and commissions" TEXT,
    "Symbol.5" TEXT,
    "Average wages, salaries and commissions" TEXT,
    "Symbol.6" TEXT,

    -- Metadata columns
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source_file TEXT,
    load_batch_id UUID,
    row_number BIGINT,

    -- surrogate key
    raw_id BIGSERIAL PRIMARY KEY
);
