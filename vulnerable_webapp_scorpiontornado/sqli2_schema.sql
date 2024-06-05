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


-- Note - this file should be hidden from CTF-doers. Figuring out the database schema is part of the challenge.
-- Read ahead at your own risk, but know that you probably won't get the SQL schema in real life, so you're
-- not helping yourself if you choose to cheat. If you do, please don't spoil the challenge for others.

-- Inspiration drawn from COMP3311 23T3 assignment 2 (https://webcms3.cse.unsw.edu.au/COMP3311/23T3/resources/89176)
-- and the COMP6841 SQLI pre-recorded video (https://youtu.be/bAhvzXfuhg8)

-- Notes:
--  Unis really do keep all this info (and more) about you: https://www.student.unsw.edu.au/privacy
--      Could've also included personal email, country of origin, program of study, fee payment info,
--      financial assistance and scholarships, disciplinary info etc. but that's too much for this CTF.
--  Also, date_of_birth is an ISO8601 string in the form "YYYY-MM-DD"
DROP TABLE IF EXISTS Students;
CREATE TABLE Students(
    student_id INTEGER CHECK (student_id BETWEEN 1000000 AND 9999999),
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone_number TEXT,
    home_address TEXT,
    date_of_birth TEXT,
    PRIMARY KEY (student_id)
);

-- Notes:
--  For 'term', could use the regex from COMP3311 23T3 assignment 2 - '[12][01239]T[0123]',
--      but sqlite doesn't distribute a regular expression implementation by default. I can't be bothered getting it working..
--  Could also define grade as something like  grade TEXT CHECK (grade IN ("HD", "DN", "CR", "PS", "FL")),
--      but this would stop me putting a flag in the grade column.
DROP TABLE IF EXISTS Marks;
CREATE TABLE Marks (
    student_id INTEGER,
    course_code TEXT,
    term TEXT,
    mark INTEGER CHECK (mark BETWEEN 0 AND 100),
    grade TEXT,
    PRIMARY KEY (student_id, course_code),
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);