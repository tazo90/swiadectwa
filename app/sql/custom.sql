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

----------------------------- Wartosci dla bazy:
insert into app_swiadectwo (nazwa, obrazek) values
('MEN-I3a2', 'uploads/form/MEN-I3a2(1).jpg'),
('MEN-I3a2', 'uploads/form/MEN-I3a2(2).jpg'),
('MEN-I21a2', 'uploads/form/MEN-I21a2(1).jpg'),
('MEN-I21a2', 'uploads/form/MEN-I21a2(2).jpg'),
('MEN-I27a2', 'uploads/form/MEN-I27a2(1).jpg'),
('MEN-I27a2', 'uploads/form/MEN-I27a2(2).jpg'),
('MEN-I27a2', 'uploads/form/MEN-I27a2(3).jpg');

insert into app_pole (id_swiad_id, nazwa, wsp_x, wsp_y, wysokosc, szerokosc, stale) values 
(1, 'first_name', 620, 1183, 44, 1262, 't'),  
(1, 'data_ur', 445, 1338, 44, 460, 't'), 
(1, 'miejsce_ur',  1017,  1338, 44, 461, 't'), 
(1, 'username',  1590,  1340, 44, 461, 't'), 
(1, 'plec',  622,  1490, 44, 75, 't'), 
(1, 'rok_szkolny',  1016,  1490, 44, 461, 'n'), 
(1, 'klasa',  1646,  1490, 44, 403, 'n'), 
(1, 'nazwa',  445,  1610, 44, 1605, 't'), 
(1, 'nr',  492,  1840, 44, 250, 't'), 
(1, 'im',  822,  1840, 44, 1227, 'n'), 
(1, 'miejscowosc',  485,  2071, 44, 633, 't'), 
(1, 'wojewodztwo',  1220,  2071, 44, 833, 't'), 
(1, 'nie',  752,  2185, 44, 101, 'n'), 
(1, 'plec',  1020,  2185, 44, 57, 't'), 
(1, 'promocja',  1238,  2185, 44, 55, 'n'), 
(1, 'nowa_klasa',  1455,  2185, 44, 306, 'n'), 
(1, 'miejscowosc_wpisu',  445,  2472, 44, 737, 'n'), 
(1, 'data_wpisu',  1300,  2472, 44, 720, 'n'), 
(1, 'Nr',  505,  2765, 44, 360, 'n'), 
(2, 'zachowanie', 1395, 557, 44, 658, 'n'), 
(2, 'religia/etyka', 1395, 623, 44, 658, 'n'), 
(2, 'jezyk_polski',  1395,  825, 44, 658, 'n'), 
(2, 'jezyk_1',  552,  895, 44, 788, 'n'), 
(2, 'jezyk_1_val',  1395,  895, 44, 658, 'n'), 
(2, 'muzyka',  1395,  967, 44, 658, 'n'), 
(2, 'plastyka',  1395,  1040, 44, 658, 'n'), 
(2, 'historia',  1395,  1115, 44, 658, 'n'), 
(2, 'przyroda',  1395,  1183, 44, 658, 'n'), 
(2, 'matematyka',  1395,  1253, 44, 658, 'n'), 
(2, 'komputerowe',  1395,  1330, 44, 658, 'n'), 
(2, 'technika',  1395,  1400, 44, 658, 'n'), 
(2, 'wf',  1395,  1470, 44, 658, 'n'), 
(2, 'prz1',  450,  1540, 44, 890, 'n'), 
(2, 'prz1_val',  1395,  1540, 44, 658, 'n'), 
(2, 'prz2',  450,  1615, 44, 890, 'n'), 
(2, 'prz2_val',  1395,  1615, 44, 658, 'n'), 
(2, 'prz3',  450,  1685, 44, 890, 'n'), 
(2, 'prz3_val',  1395,  1685, 44, 658, 'n'), 
(2, 'dod1',  450,  1864, 44, 890, 'n'), 
(2, 'dod1_val',  1395,  1864, 44, 658, 'n'), 
(2, 'dod2',  450,  1935, 44, 890, 'n'), 
(2, 'dod2_val',  1395,  1935, 44, 658, 'n'), 
(2, 'indywidualny',  450,  2190, 44, 1600, 'n'), 
(2, 'szczegolny',  450,  2477, 44, 1600, 'n'), 
(3, 'first_name', 620, 1125, 44, 1262, 't'), 
(3, 'data_ur', 445, 1280, 44, 462, 't'), 
(3, 'miejsce_ur',  1017,  1280, 44, 462, 't'), 
(3, 'username',  1590,  1280, 44, 462, 't'), 
(3, 'plec',  622,  1432, 44, 75, 't'), 
(3, 'rok_szkolny',  1016,  1432, 44, 461, 'n'), 
(3, 'klasa',  1646,  1432, 44, 403, 'n'), 
(3, 'nazwa',  445,  1535, 44, 1605, 't'), 
(3, 'nr',  492,  1722, 44, 250, 't'), 
(3, 'im',  822,  1722, 44, 1227, 'n'), 
(3, 'miejscowosc',  485,  1905, 44, 633, 't'), 
(3, 'wojewodztwo',  1220,  1905, 44, 833, 't'), 
(3, 'plec',  630,  2000, 44, 75, 't'), 
(3, 'przedmiot1',  445,  2090, 44, 760, 'n'), 
(3, 'przedmiot2',  1290,  2090, 44, 760, 'n'), 
(3, 'przedmiot3',  445,  2185, 44, 760, 'n'), 
(3, 'przedmiot4',  1290,  2185, 44, 760, 'n'), 
(3, 'nie',  752,  2370, 44, 101, 'n'), 
(3, 'plec',  1020,  2370, 44, 57, 't'), 
(3, 'promocja',  1238,  2370, 44, 55, 'n'), 
(3, 'nowa_klasa',  1455,  2370, 44, 306, 'n'), 
(3, 'miejscowosc_wpisu',  445,  2565, 44, 737, 'n'), 
(3, 'data_wpisu',  1300,  2565, 44, 720, 'n'), 
(3, 'Nr',  505,  2793, 44, 360, 'n'), 
(4, 'zachowanie', 1395, 537, 44, 658, 'n'), 
(4, 'religia/etyka', 1395, 597, 44, 658, 'n'), 
(4, 'jezyk_polski',  1395,  778, 44, 658, 'n'), 
(4, 'jezyk_1',  550,  840, 44, 770, 'n'), 
(4, 'jezyk_1_val',  1395,  840, 44, 658, 'n'), 
(4, 'jezyk_2',  550,  903, 44, 770, 'n'), 
(4, 'jezyk_2_val',  1395,  903, 44, 658, 'n'), 
(4, 'wok',  1395,  965, 44, 658, 'n'), 
(4, 'historia',  1395,  1027, 44, 658, 'n'), 
(4, 'wos',  1395,  1088, 44, 658, 'n'), 
(4, 'przedsiebiorczosc',  1395,  1151, 44, 658, 'n'), 
(4, 'geografia',  1395,  1214, 44, 658, 'n'), 
(4, 'biologia',  1395,  1276, 44, 658, 'n'), 
(4, 'chemia',  1395,  1339, 44, 658, 'n'), 
(4, 'fizyka',  1395,  1400, 44, 658, 'n'), 
(4, 'matematyka',  1395,  1464, 44, 658, 'n'), 
(4, 'informatyka',  1395,  1527, 44, 658, 'n'), 
(4, 'wf',  1395,  1589, 44, 658, 'n'), 
(4, 'bezpieczenstwo',  1395,  1650, 44, 658, 'n'), 
(4, 'prz1',  450,  1713, 44, 870, 'n'), 
(4, 'prz1_val',  1395,  1713, 44, 658, 'n'), 
(4, 'prz2',  450,  1775, 44, 870, 'n'), 
(4, 'prz2_val',  1395,  1775, 44, 658, 'n'), 
(4, 'prz3',  450,  1837, 44, 870, 'n'), 
(4, 'prz3_val',  1395,  1837, 44, 658, 'n'), 
(4, 'prz_u1',  450,  1960, 44, 870, 'n'), 
(4, 'prz_u1_val',  1395,  1960, 44, 658, 'n'), 
(4, 'prz_u2',  450,  2023, 44, 870, 'n'), 
(4, 'prz_u2_val',  1395,  2023, 44, 658, 'n'), 
(4, 'dod1',  450,  2200, 44, 870, 'n'), 
(4, 'dod1_val',  1395,  2200, 44, 658, 'n'), 
(4, 'dod2',  450,  2260, 44, 870, 'n'), 
(4, 'dod2_val',  1395,  2260, 44, 658, 'n'), 
(4, 'indywidualny',  450,  2433, 44, 1600, 'n'), 
(4, 'szczegolny',  450,  2680, 44, 1600, 'n'), 
(5, 'first_name', 620, 1125, 44, 1262, 't'), 
(5, 'data_ur', 445, 1280, 44, 462, 't'), 
(5, 'miejsce_ur',  1017,  1280, 44, 462, 't'), 
(5, 'username',  1590,  1280, 44, 462, 't'), 
(5, 'plec',  622,  1432, 44, 75, 't'), 
(5, 'rok_szkolny',  1016,  1432, 44, 461, 'n'), 
(5, 'klasa',  1646,  1432, 44, 403, 'n'), 
(5, 'nazwa',  445,  1535, 44, 1605, 't'), 
(5, 'nr',  492,  1722, 44, 250, 't'), 
(5, 'im',  822,  1722, 44, 1227, 'n'), 
(5, 'miejscowosc',  485,  1905, 44, 633, 't'), 
(5, 'wojewodztwo',  1220,  1905, 44, 833, 't'), 
(5, 'plec',  630,  2000, 44, 75, 't'), 
(5, 'przedmiot1',  445,  2090, 44, 760, 'n'), 
(5, 'przedmiot2',  1290,  2090, 44, 760, 'n'), 
(5, 'nie',  752,  2272, 44, 101, 'n'), 
(5, 'plec',  1020,  2272, 44, 57, 't'), 
(5, 'promocja',  1238,  2272, 44, 55, 'n'), 
(5, 'nowa_klasa',  1455,  2272, 44, 306, 'n'), 
(5, 'miejscowosc_wpisu',  445,  2565, 44, 737, 'n'), 
(5, 'data_wpisu',  1300,  2565, 44, 720, 'n'), 
(5, 'Nr',  505,  2793, 44, 360, 'n'), 
(6, 'zachowanie', 1400, 520, 44, 653, 'n'), 
(6, 'religia/etyka', 1400, 575, 44, 653, 'n'), 
(6, 'jezyk_polski',  1400,  735, 44, 653, 'n'), 
(6, 'jezyk_1',  1400,  788, 44, 653, 'n'), 
(6, 'jezyk_2',  1400,  843, 44, 653, 'n'), 
(6, 'wok',  1400,  898, 44, 653, 'n'), 
(6, 'historia',  1400,  949, 44, 653, 'n'), 
(6, 'wos',  1400,  1004, 44, 653, 'n'), 
(6, 'przedsiebiorczosc',  1400,  1057, 44, 653, 'n'), 
(6, 'geografia',  1400,  1113, 44, 653, 'n'), 
(6, 'biologia',  1400,  1166, 44, 653, 'n'), 
(6, 'chemia',  1400,  1220, 44, 653, 'n'), 
(6, 'fizyka',  1400,  1275, 44, 653, 'n'), 
(6, 'matematyka',  1400,  1328, 44, 653, 'n'), 
(6, 'informatyka',  1400,  1381, 44, 653, 'n'), 
(6, 'wf',  1400,  1436, 44, 653, 'n'), 
(6, 'bezpieczenstwo',  1400,  1491, 44, 653, 'n'), 
(6, 'prz1',  452,  1544, 44, 870, 'n'), 
(6, 'prz1_val',  1400,  1544, 44, 653, 'n'), 
(6, 'prz2',  452,  1597, 44, 870, 'n'), 
(6, 'prz2_val',  1400,  1597, 44, 653, 'n'), 
(6, 'prz3',  452,  1653, 44, 870, 'n'), 
(6, 'prz3_val',  1400,  1653, 44, 653, 'n'), 
(6, 'prz_u1',  452,  2898, 44, 870, 'n'), 
(6, 'prz_u1_val',  1400,  2898, 44, 653, 'n'), 
(6, 'prz_u2',  452,  2948, 44, 870, 'n'), 
(6, 'prz_u2_val',  1400,  2948, 44, 653, 'n'), 
(7, 'dod1',  448,  655, 44, 893, 'n'), 
(7, 'dod1_val',  1395,  655, 44, 658, 'n'), 
(7, 'dod2',  448,  770, 44, 893, 'n'), 
(7, 'dod2_val',  1395,  770, 44, 658, 'n'), 
(7, 'indywidualny',  448,  1178, 44, 1600, 'n'), 
(7, 'szczegolny',  448,  1690, 44, 1600, 'n');

insert into auth_user (username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined) 
values ('12345', 'Anna', 'Abacka', 'anna@co.uk', (select password from auth_user where username ='tazo'), false, true, false, 
(select last_login from auth_user where username='tazo'), (select date_joined from auth_user where username='tazo'));

update app_profil set rola='u' where user_id=(select id from auth_user where last_name='Abacka');

insert into app_szkola (nazwa, nr, miejscowosc, wojewodztwo) values ('Szkola podstawowa', 73, 'Wroclaw', 'Dolnoslaskie');

insert into app_uczen (id_user_id, data_ur, miejsce_ur, plec) values ((select id from auth_user where username='12345'), '2001-09-28', 'Wroclaw', '');

insert into app_wartosci (id_user_id, id_pole_id, wartosc) values 
((select id from auth_user where username='12345'), (select id from app_pole where nazwa='nie' and id_swiad_id=1), 'nie'),
((select id from auth_user where username='12345'), (select id from app_pole where nazwa='promocja' and id_swiad_id=1), 'i'),
((select id from auth_user where username='12345'), (select id from app_pole where nazwa='nowa_klasa' and id_swiad_id=1), 'czwartej');
