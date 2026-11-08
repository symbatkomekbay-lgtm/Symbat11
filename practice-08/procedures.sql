CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR, p_surname VARCHAR DEFAULT '')
LANGUAGE plpgsql AS $$
BEGIN
    IF NULLIF(BTRIM(p_name), '') IS NULL OR p_phone !~ '^\+?[0-9]{10,15}$' OR p_phone IS NULL THEN
        RAISE EXCEPTION 'Invalid name or phone';
    END IF;
    INSERT INTO contacts(name, surname, phone)
    VALUES (BTRIM(p_name), COALESCE(BTRIM(p_surname), ''), p_phone)
    ON CONFLICT (name) DO UPDATE
    SET phone = EXCLUDED.phone, surname = EXCLUDED.surname;
END;
$$;

-- Invalid rows are returned in the INOUT parameter as a JSON array.
-- Each input object should have name, phone, and optional surname.
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(IN p_contacts JSONB, INOUT p_invalid JSONB)
LANGUAGE plpgsql AS $$
DECLARE
    item JSONB;
    v_name TEXT;
    v_phone TEXT;
    v_surname TEXT;
BEGIN
    p_invalid := '[]'::JSONB;
    IF jsonb_typeof(p_contacts) IS DISTINCT FROM 'array' THEN
        RAISE EXCEPTION 'Input must be a JSON array';
    END IF;
    FOR item IN SELECT value FROM jsonb_array_elements(p_contacts) LOOP
        v_name := BTRIM(item->>'name');
        v_phone := item->>'phone';
        v_surname := COALESCE(BTRIM(item->>'surname'), '');
        IF NULLIF(v_name, '') IS NULL OR v_phone IS NULL OR v_phone !~ '^\+?[0-9]{10,15}$' THEN
            p_invalid := p_invalid || jsonb_build_array(item);
        ELSE
            INSERT INTO contacts(name, surname, phone)
            VALUES (v_name, v_surname, v_phone)
            ON CONFLICT (name) DO UPDATE
            SET phone = EXCLUDED.phone, surname = EXCLUDED.surname;
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF NULLIF(BTRIM(p_name), '') IS NULL AND NULLIF(BTRIM(p_phone), '') IS NULL THEN
        RAISE EXCEPTION 'Provide a name or phone';
    END IF;
    DELETE FROM contacts AS c
    WHERE (NULLIF(BTRIM(p_name), '') IS NOT NULL AND c.name = BTRIM(p_name))
       OR (NULLIF(BTRIM(p_phone), '') IS NOT NULL AND c.phone = BTRIM(p_phone));
END;
$$;
