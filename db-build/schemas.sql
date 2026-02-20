-- ============================================
-- Schema Initialization Script
-- Creates core data platform schemas
-- ============================================

BEGIN;

-- Raw: Unmodified source data
CREATE SCHEMA IF NOT EXISTS raw;

-- Staging: Cleaned / lightly transformed data
CREATE SCHEMA IF NOT EXISTS staging;

-- Analytics: Modeled / aggregated / business-ready data
CREATE SCHEMA IF NOT EXISTS analytics;

-- Serving: Views exposed to applications
CREATE SCHEMA IF NOT EXISTS serving;

COMMIT;