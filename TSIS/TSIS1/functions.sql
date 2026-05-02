CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(name TEXT, email TEXT, phone TEXT, group_name TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.name::text,
        p.email::text,
        ph.phone::text,
        g.name::text
    FROM phonebook p
    LEFT JOIN phones ph ON p.id = ph.contact_id
    LEFT JOIN groups g ON p.group_id = g.id
    WHERE 
        p.name ILIKE '%' || p_query || '%'
        OR p.email ILIKE '%' || p_query || '%'
        OR ph.phone ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_page(lim INT, off INT)
RETURNS TABLE(name VARCHAR, email VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT p.name, p.email
    FROM phonebook p
    ORDER BY p.name
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;
