-- TSIS 1: extend the existing Practice 7/8 contacts table.
CREATE TABLE IF NOT EXISTS contacts (
 id SERIAL PRIMARY KEY,
 name VARCHAR(100) UNIQUE NOT NULL,
 surname VARCHAR(100) NOT NULL DEFAULT '',
 phone VARCHAR(20) NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS groups (id SERIAL PRIMARY KEY, name VARCHAR(50) UNIQUE NOT NULL);
INSERT INTO groups(name) VALUES ('Family'),('Work'),('Friend'),('Other') ON CONFLICT (name) DO NOTHING;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS email VARCHAR(100);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS birthday DATE;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW();
UPDATE contacts SET created_at=NOW() WHERE created_at IS NULL;
CREATE TABLE IF NOT EXISTS phones (
 id SERIAL PRIMARY KEY,
 contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
 phone VARCHAR(20) NOT NULL,
 type VARCHAR(10) NOT NULL CHECK(type IN ('home','work','mobile')),
 UNIQUE(contact_id,phone)
);
-- One-time migration of legacy phone values. Safe to run repeatedly.
INSERT INTO phones(contact_id,phone,type)
SELECT id,phone,'mobile' FROM contacts WHERE phone IS NOT NULL AND phone <> ''
ON CONFLICT(contact_id,phone) DO NOTHING;
