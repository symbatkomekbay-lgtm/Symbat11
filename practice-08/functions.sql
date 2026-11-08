CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    surname VARCHAR(100) NOT NULL DEFAULT '',
    phone VARCHAR(20) NOT NULL
);

CREATE OR REPLACE FUNCTION search_contacts(p_pattern TEXT)
RETURNS TABLE(id INTEGER, name VARCHAR, surname VARCHAR, phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.surname, c.phone
    FROM contacts AS c
    WHERE c.name ILIKE '%' || p_pattern || '%'
       OR c.surname ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%'
    ORDER BY c.id;
END;
$$;

CREATE OR REPLACE FUNCTION paginated_contacts(p_limit INTEGER, p_offset INTEGER)
RETURNS TABLE(id INTEGER, name VARCHAR, surname VARCHAR, phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_limit <= 0 OR p_offset < 0 THEN
        RAISE EXCEPTION 'Limit must be positive and offset cannot be negative';
    END IF;
    RETURN QUERY
    SELECT c.id, c.name, c.surname, c.phone
    FROM contacts AS c
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$;
