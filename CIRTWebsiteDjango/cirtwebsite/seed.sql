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
INSERT INTO docs (title, author, file_type, file_size, category_id, subcategory_id, file_url)
VALUES ('Order on Sanctions in Wadsworth v. Walmart Inc et al', 'Margaret Botkins', 'PDF', 265, 1, 2, 'https://criminology-db-bucket.s3.us-east-1.amazonaws.com/court-records/Order-on-Sanctions-in-Wadsworth-v.-Walmart-Inc-et-al.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAW3MECIUL4M4W5TGG%2F20250307%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250307T003712Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIAY%2BxE5r0419hgYu14rRbMFuOXg4EbVcjnH0lls84ScqAiAMo1Ax3sda6C5XLTiPQfi%2B%2FJu4CjwfWrUZtcJqzwiJkyrsAgg6EAAaDDQ3MTExMjc2MjY0NyIM6U%2FVvCfMsR7AjIqgKskCAzT%2FNMKvdBn0l%2BrV3SLGMMsv7E5zsrUVWNFg1hpPgwr6DWrlGHLEkisn7FPYH8dK9Ht9EOkcwnDfMYf4ohYY4JncyJ6endnLHz5ODdajiHSE8hezkftOZ0kx5yaFKKLVD08eeEoJqNDW6ejU5mqqsjtgkz1hXlao5waTqWz3qhCmDhu6PUDe%2FF3gd6G5kOJkyWEQvRgmz8eZ5p%2B%2FiHGbqSGLJVI07Cb2pTaQkNCSKLrbpfJP6futCtytlyi%2BCotZH2VzNg6k4YPwJJ2Ry4sOHtoleU2sOK2PKWP4NI%2BdaBqxd6sdJm4lxg6Gr9IspIfn4eDTe4a27txUgM%2B%2FOhF7ruuQ5HCcVVQwYYubmYs8mxy6ExX4gMks3ngFPsj8nvZXZOSuu%2FX%2BOcJMgJHZaq9msMp3oqS06hrl6lQ3ZG2dJMray77k7OTJn18wkv%2BovgY6tALCpOaEwYERUVT9GKVG793vI%2Bo9gegBKefZ9jS%2B5H9xSAm1knWD4jfeKplZR3REE11pMWFWqLnhXd1PRXXXHnPZbIp%2FvpZF2Bd3Bw72FmZBjSGBkAeqNfzwCdKwpRA%2BTBCORYOX4waNTAyYaa2LGOdYg9kYgOSFpW9LeraFqZyH%2Bkt0JjXL%2Bn0eTpBrL9wqiMAR90lG6xP14w7NTXyQOCWavSuTruaQ183%2BvpWTTHkqUquK3LJ8p0%2BpZVJeUafro3RAKy0kjntQznQf5tAVKzCvYpRdIdnJWOJt4FhVHM%2BuWsjMa2YHFodmaZcLc7DbXzUXNNajd710nWaqDCT2B9Ottw8ZYpX%2FdR098sS1yjH3hPHIVPsgapi1SivJgbF7yObz%2FVJ8g%2F0y3OKn29L68TyTEzU3iA%3D%3D&X-Amz-Signature=c5ac1473ddae43046939443e0832c9fd932030d3010a347222bc7bcbd52a30f4&X-Amz-SignedHeaders=host&response-content-disposition=inline')

INSERT INTO docs (title, author, file_type, file_size, category_id, subcategory_id, file_url)
VALUES ('Order on Sanctions in Wadsworth v. Walmart Inc et al', 'Margaret Botkins', 'PDF', 265, 1, 2, 'https://criminology-db-bucket.s3.us-east-1.amazonaws.com/court-records/Order-on-Sanctions-in-Wadsworth-v.-Walmart-Inc-et-al.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAW3MECIUL4M4W5TGG%2F20250307%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250307T003712Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIAY%2BxE5r0419hgYu14rRbMFuOXg4EbVcjnH0lls84ScqAiAMo1Ax3sda6C5XLTiPQfi%2B%2FJu4CjwfWrUZtcJqzwiJkyrsAgg6EAAaDDQ3MTExMjc2MjY0NyIM6U%2FVvCfMsR7AjIqgKskCAzT%2FNMKvdBn0l%2BrV3SLGMMsv7E5zsrUVWNFg1hpPgwr6DWrlGHLEkisn7FPYH8dK9Ht9EOkcwnDfMYf4ohYY4JncyJ6endnLHz5ODdajiHSE8hezkftOZ0kx5yaFKKLVD08eeEoJqNDW6ejU5mqqsjtgkz1hXlao5waTqWz3qhCmDhu6PUDe%2FF3gd6G5kOJkyWEQvRgmz8eZ5p%2B%2FiHGbqSGLJVI07Cb2pTaQkNCSKLrbpfJP6futCtytlyi%2BCotZH2VzNg6k4YPwJJ2Ry4sOHtoleU2sOK2PKWP4NI%2BdaBqxd6sdJm4lxg6Gr9IspIfn4eDTe4a27txUgM%2B%2FOhF7ruuQ5HCcVVQwYYubmYs8mxy6ExX4gMks3ngFPsj8nvZXZOSuu%2FX%2BOcJMgJHZaq9msMp3oqS06hrl6lQ3ZG2dJMray77k7OTJn18wkv%2BovgY6tALCpOaEwYERUVT9GKVG793vI%2Bo9gegBKefZ9jS%2B5H9xSAm1knWD4jfeKplZR3REE11pMWFWqLnhXd1PRXXXHnPZbIp%2FvpZF2Bd3Bw72FmZBjSGBkAeqNfzwCdKwpRA%2BTBCORYOX4waNTAyYaa2LGOdYg9kYgOSFpW9LeraFqZyH%2Bkt0JjXL%2Bn0eTpBrL9wqiMAR90lG6xP14w7NTXyQOCWavSuTruaQ183%2BvpWTTHkqUquK3LJ8p0%2BpZVJeUafro3RAKy0kjntQznQf5tAVKzCvYpRdIdnJWOJt4FhVHM%2BuWsjMa2YHFodmaZcLc7DbXzUXNNajd710nWaqDCT2B9Ottw8ZYpX%2FdR098sS1yjH3hPHIVPsgapi1SivJgbF7yObz%2FVJ8g%2F0y3OKn29L68TyTEzU3iA%3D%3D&X-Amz-Signature=c5ac1473ddae43046939443e0832c9fd932030d3010a347222bc7bcbd52a30f4&X-Amz-SignedHeaders=host&response-content-disposition=inline')
INSERT INTO docs (title, author, file_type, file_size, category_id, subcategory_id, file_url)
VALUES ('Analysis of Financial Markets in 2025', 'James Richardson', 'PDF', 245, 3, 4, 'https://criminology-db-bucket.s3.us-east-1.amazonaws.com/court-records/Order-on-Sanctions-in-Wadsworth-v.-Walmart-Inc-et-al.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAW3MECIUL4M4W5TGG%2F20250307%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250307T003712Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIAY%2BxE5r0419hgYu14rRbMFuOXg4EbVcjnH0lls84ScqAiAMo1Ax3sda6C5XLTiPQfi%2B%2FJu4CjwfWrUZtcJqzwiJkyrsAgg6EAAaDDQ3MTExMjc2MjY0NyIM6U%2FVvCfMsR7AjIqgKskCAzT%2FNMKvdBn0l%2BrV3SLGMMsv7E5zsrUVWNFg1hpPgwr6DWrlGHLEkisn7FPYH8dK9Ht9EOkcwnDfMYf4ohYY4JncyJ6endnLHz5ODdajiHSE8hezkftOZ0kx5yaFKKLVD08eeEoJqNDW6ejU5mqqsjtgkz1hXlao5waTqWz3qhCmDhu6PUDe%2FF3gd6G5kOJkyWEQvRgmz8eZ5p%2B%2FiHGbqSGLJVI07Cb2pTaQkNCSKLrbpfJP6futCtytlyi%2BCotZH2VzNg6k4YPwJJ2Ry4sOHtoleU2sOK2PKWP4NI%2BdaBqxd6sdJm4lxg6Gr9IspIfn4eDTe4a27txUgM%2B%2FOhF7ruuQ5HCcVVQwYYubmYs8mxy6ExX4gMks3ngFPsj8nvZXZOSuu%2FX%2BOcJMgJHZaq9msMp3oqS06hrl6lQ3ZG2dJMray77k7OTJn18wkv%2BovgY6tALCpOaEwYERUVT9GKVG793vI%2Bo9gegBKefZ9jS%2B5H9xSAm1knWD4jfeKplZR3REE11pMWFWqLnhXd1PRXXXHnPZbIp%2FvpZF2Bd3Bw72FmZBjSGBkAeqNfzwCdKwpRA%2BTBCORYOX4waNTAyYaa2LGOdYg9kYgOSFpW9LeraFqZyH%2Bkt0JjXL%2Bn0eTpBrL9wqiMAR90lG6xP14w7NTXyQOCWavSuTruaQ183%2BvpWTTHkqUquK3LJ8p0%2BpZVJeUafro3RAKy0kjntQznQf5tAVKzCvYpRdIdnJWOJt4FhVHM%2BuWsjMa2YHFodmaZcLc7DbXzUXNNajd710nWaqDCT2B9Ottw8ZYpX%2FdR098sS1yjH3hPHIVPsgapi1SivJgbF7yObz%2FVJ8g%2F0y3OKn29L68TyTEzU3iA%3D%3D&X-Amz-Signature=c5ac1473ddae43046939443e0832c9fd932030d3010a347222bc7bcbd52a30f4&X-Amz-SignedHeaders=host&response-content-disposition=inline')
INSERT INTO docs (title, author, file_type, file_size, category_id, subcategory_id, file_url)
VALUES ('Scientific Exploration of Ocean Depths', 'Laura Sinclair', 'PDF', 370, 2, 3, 'https://criminology-db-bucket.s3.us-east-1.amazonaws.com/court-records/Order-on-Sanctions-in-Wadsworth-v.-Walmart-Inc-et-al.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAW3MECIUL4M4W5TGG%2F20250307%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250307T003712Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIAY%2BxE5r0419hgYu14rRbMFuOXg4EbVcjnH0lls84ScqAiAMo1Ax3sda6C5XLTiPQfi%2B%2FJu4CjwfWrUZtcJqzwiJkyrsAgg6EAAaDDQ3MTExMjc2MjY0NyIM6U%2FVvCfMsR7AjIqgKskCAzT%2FNMKvdBn0l%2BrV3SLGMMsv7E5zsrUVWNFg1hpPgwr6DWrlGHLEkisn7FPYH8dK9Ht9EOkcwnDfMYf4ohYY4JncyJ6endnLHz5ODdajiHSE8hezkftOZ0kx5yaFKKLVD08eeEoJqNDW6ejU5mqqsjtgkz1hXlao5waTqWz3qhCmDhu6PUDe%2FF3gd6G5kOJkyWEQvRgmz8eZ5p%2B%2FiHGbqSGLJVI07Cb2pTaQkNCSKLrbpfJP6futCtytlyi%2BCotZH2VzNg6k4YPwJJ2Ry4sOHtoleU2sOK2PKWP4NI%2BdaBqxd6sdJm4lxg6Gr9IspIfn4eDTe4a27txUgM%2B%2FOhF7ruuQ5HCcVVQwYYubmYs8mxy6ExX4gMks3ngFPsj8nvZXZOSuu%2FX%2BOcJMgJHZaq9msMp3oqS06hrl6lQ3ZG2dJMray77k7OTJn18wkv%2BovgY6tALCpOaEwYERUVT9GKVG793vI%2Bo9gegBKefZ9jS%2B5H9xSAm1knWD4jfeKplZR3REE11pMWFWqLnhXd1PRXXXHnPZbIp%2FvpZF2Bd3Bw72FmZBjSGBkAeqNfzwCdKwpRA%2BTBCORYOX4waNTAyYaa2LGOdYg9kYgOSFpW9LeraFqZyH%2Bkt0JjXL%2Bn0eTpBrL9wqiMAR90lG6xP14w7NTXyQOCWavSuTruaQ183%2BvpWTTHkqUquK3LJ8p0%2BpZVJeUafro3RAKy0kjntQznQf5tAVKzCvYpRdIdnJWOJt4FhVHM%2BuWsjMa2YHFodmaZcLc7DbXzUXNNajd710nWaqDCT2B9Ottw8ZYpX%2FdR098sS1yjH3hPHIVPsgapi1SivJgbF7yObz%2FVJ8g%2F0y3OKn29L68TyTEzU3iA%3D%3D&X-Amz-Signature=c5ac1473ddae43046939443e0832c9fd932030d3010a347222bc7bcbd52a30f4&X-Amz-SignedHeaders=host&response-content-disposition=inline')
INSERT INTO docs (title, author, file_type, file_size, category_id, subcategory_id, file_url)
VALUES ('Introduction to Machine Learning Algorithms', 'Michael Schwartz', 'PDF', 200, 4, 1, 'https://criminology-db-bucket.s3.us-east-1.amazonaws.com/court-records/Order-on-Sanctions-in-Wadsworth-v.-Walmart-Inc-et-al.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAW3MECIUL4M4W5TGG%2F20250307%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250307T003712Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIAY%2BxE5r0419hgYu14rRbMFuOXg4EbVcjnH0lls84ScqAiAMo1Ax3sda6C5XLTiPQfi%2B%2FJu4CjwfWrUZtcJqzwiJkyrsAgg6EAAaDDQ3MTExMjc2MjY0NyIM6U%2FVvCfMsR7AjIqgKskCAzT%2FNMKvdBn0l%2BrV3SLGMMsv7E5zsrUVWNFg1hpPgwr6DWrlGHLEkisn7FPYH8dK9Ht9EOkcwnDfMYf4ohYY4JncyJ6endnLHz5ODdajiHSE8hezkftOZ0kx5yaFKKLVD08eeEoJqNDW6ejU5mqqsjtgkz1hXlao5waTqWz3qhCmDhu6PUDe%2FF3gd6G5kOJkyWEQvRgmz8eZ5p%2B%2FiHGbqSGLJVI07Cb2pTaQkNCSKLrbpfJP6futCtytlyi%2BCotZH2VzNg6k4YPwJJ2Ry4sOHtoleU2sOK2PKWP4NI%2BdaBqxd6sdJm4lxg6Gr9IspIfn4eDTe4a27txUgM%2B%2FOhF7ruuQ5HCcVVQwYYubmYs8mxy6ExX4gMks3ngFPsj8nvZXZOSuu%2FX%2BOcJMgJHZaq9msMp3oqS06hrl6lQ3ZG2dJMray77k7OTJn18wkv%2BovgY6tALCpOaEwYERUVT9GKVG793vI%2Bo9gegBKefZ9jS%2B5H9xSAm1knWD4jfeKplZR3REE11pMWFWqLnhXd1PRXXXHnPZbIp%2FvpZF2Bd3Bw72FmZBjSGBkAeqNfzwCdKwpRA%2BTBCORYOX4waNTAyYaa2LGOdYg9kYgOSFpW9LeraFqZyH%2Bkt0JjXL%2Bn0eTpBrL9wqiMAR90lG6xP14w7NTXyQOCWavSuTruaQ183%2BvpWTTHkqUquK3LJ8p0%2BpZVJeUafro3RAKy0kjntQznQf5tAVKzCvYpRdIdnJWOJt4FhVHM%2BuWsjMa2YHFodmaZcLc7DbXzUXNNajd710nWaqDCT2B9Ottw8ZYpX%2FdR098sS1yjH3hPHIVPsgapi1SivJgbF7yObz%2FVJ8g%2F0y3OKn29L68TyTEzU3iA%3D%3D&X-Amz-Signature=c5ac1473ddae43046939443e0832c9fd932030d3010a347222bc7bcbd52a30f4&X-Amz-SignedHeaders=host&response-content-disposition=inline')

