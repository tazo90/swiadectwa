CREATE FUNCTION ins_to_group() RETURNS trigger AS $ins_to_group$
    DECLARE
       gr_id INTEGER;
    BEGIN
        IF (NEW.rola = 'u') THEN
             SELECT id INTO gr_id FROM auth_group where name = 'uczen'; 
             INSERT INTO auth_user_groups (user_id, group_id) VALUES (NEW.user_id, gr_id); 
        END IF;
        IF (NEW.rola = 'n') THEN
             SELECT id INTO gr_id FROM auth_group where name = 'nauczyciel';
             INSERT INTO auth_user_groups (user_id, group_id) VALUES (NEW.user_id, gr_id); 
        END IF;
        RETURN NEW;
    END;
$ins_to_group$ LANGUAGE plpgsql;

CREATE TRIGGER ins_to_group AFTER INSERT ON app_profil
    FOR EACH ROW EXECUTE PROCEDURE ins_to_group();


-----------------------------
insert into auth_group(name) values('uczen');
insert into auth_group(name) values('nauczyciel');

---------------------------- Prawa dla grup
insert into auth_group_permissions(group_id, permission_id) values(2, 23);
insert into auth_group_permissions(group_id, permission_id) values(2, 26);
insert into auth_group_permissions(group_id, permission_id) values(2, 34);
insert into auth_group_permissions(group_id, permission_id) values(2, 35);
insert into auth_group_permissions(group_id, permission_id) values(2, 36);
