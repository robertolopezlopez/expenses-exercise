-- Intentionally denormalized for this small dataset: department and
-- expense_type names are repeated across rows instead of referencing
-- lookup tables. This avoids expensive joins on reads.
-- A normalized model would use departments(id, name) and
-- expense_types(id, name) with foreign keys.
-- Duplicate (department, expense_type, year, month) rows are valid,
-- as the provided Expenses.csv shows.
CREATE TABLE expenses (
    -- db generated id, always (postgresql)
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department   VARCHAR(40) NOT NULL,
    expense_type VARCHAR(20) NOT NULL,
    year            SMALLINT NOT NULL CHECK (year BETWEEN 1900 AND 9999),
    month           SMALLINT NOT NULL CHECK (month BETWEEN 1 AND 12),
    amount          BIGINT NOT NULL
);

CREATE INDEX expenses_department_year_month_idx
    ON expenses (department, year, month);