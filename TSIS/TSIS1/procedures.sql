CREATE OR REPLACE PROCEDURE add_phone(
    p_name TEXT,
    p_phone TEXT,
    p_type TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE cid INT;
BEGIN
    SELECT id INTO cid FROM phonebook WHERE name = p_name;

    IF cid IS NULL THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (cid, p_phone, p_type);
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(
    p_name TEXT,
    p_group TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE gid INT;
BEGIN
    SELECT id INTO gid FROM groups WHERE name = p_group;

    IF gid IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group) RETURNING id INTO gid;
    END IF;

    UPDATE phonebook SET group_id = gid WHERE name = p_name;
END;
$$;