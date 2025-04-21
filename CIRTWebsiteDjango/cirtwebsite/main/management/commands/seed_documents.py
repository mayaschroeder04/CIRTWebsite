from django.core.management.base import BaseCommand
from main.models import Category, Subcategory, Document, CustomUser

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Categories and subcategories
        categories_with_subs = {
            'Court Records': ['Witness Testimonies', 'Case Rulings', 'Court Orders', 'Sentencing Records', 'Transcripts'],
            'Academic Papers': ['Research Articles', 'Dissertations', 'Conference Papers', 'Theses', 'Literature Reviews'],
            'Forensic Reports': ['Toxicology Reports', 'Autopsy Reports', 'Ballistics Analysis', 'DNA Analysis', 'Crime Scene Reports'],
            'Government Documents': ['Policy Briefs', 'Legislation', 'Regulatory Documents', 'Public Reports', 'Government Press Releases'],
            'Case Studies': ['Legal Case Studies', 'Medical Case Studies', 'Business Case Studies', 'Sociological Case Studies', 'Criminal Justice Case Studies'],
            'Victimology and Sociology Reports': ['Victim Impact Statements', 'Sociological Research', 'Crime Victimization Reports', 'Domestic Violence Studies', 'Social Inequality Research']
        }

        for category_name, subcats in categories_with_subs.items():
            category, _ = Category.objects.get_or_create(name=category_name)
            for subcat in subcats:
                Subcategory.objects.get_or_create(name=subcat, category=category)  # Fixed line

        # Admin user
        CustomUser.objects.get_or_create(
            username='pmalmgren',
            defaults={
                'email': 'parker@themalmgrens.com',
                'role': 'admin'
            }
        )

        # Documents
        doc_data = [
            ('Order on Sanctions in Wadsworth v. Walmart Inc et al', 'Margaret Botkins', 'Walamrt is amazing', 'PDF', 265, 'Court Records', 'Case Rulings'),
            ('Order on Sanctions in Wadsworth v. Walmart Inc et al', 'Margaret Botkins', 'Walmart sucks', 'PDF', 265, 'Court Records', 'Case Rulings'),
            ('Analysis of Financial Markets in 2025', 'James Richardson', 'Greatest economy in the world', 'PDF', 245, 'Forensic Reports', 'DNA Analysis'),
            ('Scientific Exploration of Ocean Depths', 'Laura Sinclair', 'Ocean go crazy', 'PDF', 370, 'Academic Papers', 'Conference Papers'),
            ('Introduction to Machine Learning Algorithms', 'Michael Schwartz', 'ML is nuts', 'PDF', 200, 'Government Documents', 'Policy Briefs')
        ]

        for title, author, description, file_type, file_size, cat_name, subcat_name in doc_data:
            category = Category.objects.get(name=cat_name)
            # Use category instead of category_id
            subcategory = Subcategory.objects.get(name=subcat_name, category=category)  # Fixed line
            Document.objects.get_or_create(
                title=title,
                author=author,
                defaults={
                    'description': description,
                    'file_type': file_type,
                    'file_size': file_size,
                    'category': category,
                    'subcategory': subcategory,
                    'status': 'approved',
                    'file_url': 'journal/Court-Records/Order-on-Sanctions-in-Wadsworth-v.-Walmart-Inc-et-al (1).pdf'
                }
            )

        self.stdout.write(self.style.SUCCESS("Categories, subcategories, user, and documents seeded successfully."))
