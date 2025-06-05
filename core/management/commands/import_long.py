import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from core.utils import MongoHelper

#TODO: can combine this with import_cross.py and get the model from the command line
class Command(BaseCommand):
    help = "Import long data from csv file"
    
    def add_arguments(self, parser):
        default_path = os.path.join(settings.BASE_DIR, 'data', 'long.csv')
        parser.add_argument('fp', type=str, help="Path to csv file", default=default_path)
        
    def handle(self, *args, **options) -> str | None:
        collection = MongoHelper().collection("core_long")
        file_path =  options['fp']
        if not file_path.endswith('.csv'):
            raise CommandError("File must be in csv format.")
        self.stdout.write(self.style.SUCCESS(f"Importing data from {file_path}..."))
        df = pd.read_csv(file_path)
        collection.insert_many(df.to_dict(orient='records'))
        self.stdout.write(self.style.SUCCESS("Data imported successfully."))
        