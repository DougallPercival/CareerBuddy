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
    "Work activity during the reference year (9)" TEXT,
    "Age (15A)" TEXT,
    "Gender (3)" TEXT,
    "Statistics (3)" TEXT,
    "Occupation - Minor group - National Occupational Classification (NOC) 2021 (309A)" TEXT,
    "Coordinate" TEXT,
    "Employment income statistics (7):Total - Employment income statistics[1]" TEXT,
    "Symbol" TEXT,
    "Employment income statistics (7):With employment income[2]" TEXT,
    "Symbol.1" TEXT,
    "Employment income statistics (7):Median employment income ($)[3]" TEXT,
    "Symbol.2" TEXT,
    "Employment income statistics (7):Average employment income ($)[4]" TEXT,
    "Symbol.3" TEXT,
    "Employment income statistics (7):With wages, salaries and commissions[5]" TEXT,
    "Symbol.4" TEXT,
    "Employment income statistics (7):Median wages, salaries and commissions ($)[6]" TEXT,
    "Symbol.5" TEXT,
    "Employment income statistics (7):Average wages, salaries and commissions ($)[7]" TEXT,
    "Symbol.6" TEXT,

    -- Metadata columns
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source_file TEXT,
    load_batch_id UUID,
    row_number BIGINT,

    -- surrogate key
    raw_id BIGSERIAL PRIMARY KEY
);
