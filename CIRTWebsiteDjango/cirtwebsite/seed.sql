-- Insert categories
INSERT INTO categories (name)  VALUES
    ('Court Records'),
    ('Academic Papers'),
    ('Forensic Reports'),
    ('Government Documents'),
    ('Case Studies'),
    ('Victimology and Sociology Reports');

-- Insert subcategories for 'Court Records' (category_id = 1)
SET @court_records_id = (SELECT id FROM categories WHERE name = 'Court Records');
INSERT INTO subcategories (name, category_id)
VALUES
    ('Witness Testimonies', @court_records_id),
    ('Case Rulings', @court_records_id),
    ('Court Orders', @court_records_id),
    ('Sentencing Records', @court_records_id),
    ('Transcripts', @court_records_id);

-- Insert subcategories 'Acedmic Papers' (category_id = 2)
SET @academic_papers_id = (SELECT id FROM categories WHERE name = 'Academic Papers');
INSERT INTO subcategories (name, category_id)
VALUES
    ('Research Articles', @academic_papers_id),
    ('Dissertations', @academic_papers_id),
    ('Conference Papers', @academic_papers_id),
    ('Theses', @academic_papers_id),
    ('Literature Reviews', @academic_papers_id);

-- Insert subcategories for 'Forensic Reports' (category_id = 3)
SET @forensic_reports_id = (SELECT id FROM categories WHERE name = 'Forensic Reports');
INSERT INTO subcategories (name, category_id)
VALUES
    ('Toxicology Reports', @forensic_reports_id),
    ('Autopsy Reports', @forensic_reports_id),
    ('Ballistics Analysis', @forensic_reports_id),
    ('DNA Analysis', @forensic_reports_id),
    ('Crime Scene Reports', @forensic_reports_id);

-- Insert into 'Government Documents' (category_id = 4)
-- Get the category_id for 'Government Documents'
SET @government_documents_id = (SELECT id FROM categories WHERE name = 'Government Documents');

-- Insert subcategories for 'Government Documents'
INSERT INTO subcategories (name, category_id) VALUES
    ('Policy Briefs', @government_documents_id),
    ('Legislation', @government_documents_id),
    ('Regulatory Documents', @government_documents_id),
    ('Public Reports', @government_documents_id),
    ('Government Press Releases', @government_documents_id);


-- Insert into 'Case Studies' (category = 5)
-- Get the category_id for 'Case Studies'
SET @case_studies_id = (SELECT id FROM categories WHERE name = 'Case Studies');

-- Insert subcategories for 'Case Studies'
INSERT INTO subcategories (name, category_id) VALUES
    ('Legal Case Studies', @case_studies_id),
    ('Medical Case Studies', @case_studies_id),
    ('Business Case Studies', @case_studies_id),
    ('Sociological Case Studies', @case_studies_id),
    ('Criminal Justice Case Studies', @case_studies_id);

-- Insert into 'Victimology and Sociology Reports' (category_id = 6)
-- Get the category_id for 'Victimology and Sociology Reports'
SET @victimology_reports_id = (SELECT id FROM categories WHERE name = 'Victimology and Sociology Reports');

-- Insert subcategories for 'Victimology and Sociology Reports'
INSERT INTO subcategories (name, category_id) VALUES
    ('Victim Impact Statements', @victimology_reports_id),
    ('Sociological Research', @victimology_reports_id),
    ('Crime Victimization Reports', @victimology_reports_id),
    ('Domestic Violence Studies', @victimology_reports_id),
    ('Social Inequality Research', @victimology_reports_id);




INSERT INTO users( username, email, password_hash, role )
VALUES ('pmalmgren', 'parker@themalmgrens.com', 'password', 'admin');

-- INSERT INTO documents( TITLE, AUTHOR, FILE_URL, FILE_SIZE, FILE_TYPE, USER_ID)
-- VALUES ('Criminal Behaviour Analysis', 'Dr. Smith', 'https://s3.amazonaws.com/mybucket/crime_report.pdf', 523438,'pdf', 1);

-- SELECT * FROM docs;
INSERT INTO documents (title, author, description, file_type, file_size, category_id, subcategory_id, file_url)
VALUES ('Order on Sanctions in Wadsworth v. Walmart Inc et al', 'Margaret Botkins', 'Walamrt is amazing','PDF', 265, 1, 2, 'Court-Records/Order-on-Sanctions-in-Wadsworth-v.-Walmart-Inc-et-al (1).pdf');
INSERT INTO documents (title, author, description, file_type, file_size, category_id, subcategory_id, file_url)
VALUES ('Order on Sanctions in Wadsworth v. Walmart Inc et al', 'Margaret Botkins', 'Walmart sucks','PDF', 265, 1, 2, 'Court-Records/Order-on-Sanctions-in-Wadsworth-v.-Walmart-Inc-et-al (1).pdf');
INSERT INTO documents (title, author, description, file_type, file_size, category_id, subcategory_id, file_url)
VALUES ('Analysis of Financial Markets in 2025', 'James Richardson', 'Greatest economy in the world','PDF', 245, 3, 4, 'Court-Records/Order-on-Sanctions-in-Wadsworth-v.-Walmart-Inc-et-al (1).pdf');
INSERT INTO documents (title, author, description, file_type, file_size, category_id, subcategory_id, file_url)
VALUES ('Scientific Exploration of Ocean Depths', 'Laura Sinclair','Ocean go crazy' ,'PDF', 370, 2, 3, 'Court-Records/Order-on-Sanctions-in-Wadsworth-v.-Walmart-Inc-et-al (1).pdf');
INSERT INTO documents (title, author, description, file_type, file_size, category_id, subcategory_id, file_url)
VALUES ('Introduction to Machine Learning Algorithms', 'Michael Schwartz', 'ML is nuts','PDF', 200, 4, 1, 'Court-Records/Order-on-Sanctions-in-Wadsworth-v.-Walmart-Inc-et-al (1).pdf')
