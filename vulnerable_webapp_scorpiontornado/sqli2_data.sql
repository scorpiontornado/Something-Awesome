-- Something Awesome (AKA Vulnerable Webapp, nlangford-vulnerable-webapp or nlangford-sqli)
-- An intentionally vulnerable web-app, as a teaching tool for cybersecurity.
-- Copyright (C) 2024  Nicholas Langford
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <https://www.gnu.org/licenses/>.


-- No peaking :P

INSERT INTO Students VALUES (
    5456712,
    "Hunter",
    "Dos",
    "s5456712@ad.uni.edu",
    "0412345678",
    "123 Fake Street, Kensington, NSW 2033",
    "2000-01-01"
);
INSERT INTO Students VALUES (
    5456713,
    "Huntress",
    "Deux",
    "s5456713@ad.uni.edu",
    "0487654321",
    "123 Fake Street, Kensington, NSW 2033", -- ooooh, spicy
    "2000-09-09"
);
INSERT INTO Students VALUES (
    5123456,
    "Robert",
    "Tables",
    "s5123456@ad.uni.edu",
    "0420212121",
    "SAP{STALKER_ALERT}",
    "1981-11-17"
);
INSERT INTO Students VALUES (
    5387214,
    "Roberta",
    "Tables",
    "s5387214@ad.uni.edu",
    "0498201983",
    "12 Epic Street, Kensington, NSW 2033",
    "2005-07-09"
);

INSERT INTO Marks VALUES (
    5456712,
    "COMP1511",
    "20T1",
    98,
    "HD"
);
INSERT INTO Marks VALUES (
    5456712,
    "COMP1521",
    "20T2",
    100,
    "SAP{SMARTY_PANTS}"
);
INSERT INTO Marks VALUES (
    5456712,
    "COMP2521",
    "20T2",
    93,
    "HD"
);
INSERT INTO Marks VALUES (
    5456712,
    "COMP1531",
    "20T3",
    52,
    "PS"
);
INSERT INTO Marks VALUES (
    5456712,
    "COMP3311",
    "20T3",
    97,
    "PS"
);
INSERT INTO Marks VALUES (
    5456712,
    "COMP6841",
    "21T3",
    95,
    "HD"
);
INSERT INTO Marks VALUES (
    5456713,
    "COMP1511",
    "21T2",
    70,
    "CR"
);
INSERT INTO Marks VALUES (
    5456713,
    "COMP6841",
    "21T3",
    68,
    "CR"
);
-- Alright that's enough for the sake of brevity. Would have more IRL.