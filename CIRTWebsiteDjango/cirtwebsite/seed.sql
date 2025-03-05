INSERT INTO users( username, email, password_hash, role )
VALUES ('pmalmgren', 'parker@themalmgrens.com', 'password', 'admin');

INSERT INTO documents( TITLE, AUTHOR, FILE_URL, FILE_SIZE, FILE_TYPE, USER_ID)
VALUES ('Criminal Behaviour Analysis', 'Dr. Smith', 'https://s3.amazonaws.com/mybucket/crime_report.pdf', 523438,'pdf', 1);

SELECT * FROM documents;
