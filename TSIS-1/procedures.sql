CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR,p_phone VARCHAR,p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_id INT;
BEGIN
 IF p_type NOT IN ('home','work','mobile') THEN RAISE EXCEPTION 'Invalid phone type'; END IF;
 IF p_phone IS NULL OR p_phone !~ '^\+?[0-9]{10,15}$' THEN RAISE EXCEPTION 'Invalid phone number'; END IF;
 SELECT id INTO v_id FROM contacts WHERE name=p_contact_name;
 IF v_id IS NULL THEN RAISE EXCEPTION 'Contact % not found',p_contact_name; END IF;
 INSERT INTO phones(contact_id,phone,type) VALUES(v_id,p_phone,p_type)
 ON CONFLICT(contact_id,phone) DO UPDATE SET type=EXCLUDED.type;
END $$;

CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR,p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_group_id INT;
BEGIN
 IF NULLIF(TRIM(p_group_name),'') IS NULL THEN RAISE EXCEPTION 'Group name required'; END IF;
 INSERT INTO groups(name) VALUES(TRIM(p_group_name)) ON CONFLICT(name) DO NOTHING;
 SELECT id INTO v_group_id FROM groups WHERE name=TRIM(p_group_name);
 UPDATE contacts SET group_id=v_group_id WHERE name=p_contact_name;
 IF NOT FOUND THEN RAISE EXCEPTION 'Contact % not found',p_contact_name; END IF;
END $$;

-- Replace Practice 8 function with a compatible extended search signature.
DROP FUNCTION IF EXISTS search_contacts(TEXT);
CREATE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INT,name VARCHAR(100),surname VARCHAR(100),phone VARCHAR(20))
LANGUAGE sql STABLE AS $$
 SELECT c.id,c.name,c.surname,c.phone FROM contacts c
 WHERE c.name ILIKE '%'||p_query||'%'
 OR c.surname ILIKE '%'||p_query||'%'
 OR c.email ILIKE '%'||p_query||'%'
 OR EXISTS (SELECT 1 FROM phones p WHERE p.contact_id=c.id AND p.phone ILIKE '%'||p_query||'%')
 ORDER BY c.id
$$;
