import os
import pandas as pd
from pymongo import MongoClient
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = "Import cross data from csv file"
    
    def add_arguments(self, parser):
        default_path = os.path.join(settings.BASE_DIR, 'data', 'cross.csv')
        parser.add_argument('fp', type=str, help="Path to csv file", default=default_path)
        
    def handle(self, *args, **options) -> str | None:
        client = MongoClient(os.getenv("MONGO_HOST"))
        db = client["daria-db"]
        collection = db["core_cross"]
        file_path =  options['fp']
        if not file_path.endswith('.csv'):
            raise CommandError("File must be in csv format.")
        self.stdout.write(self.style.SUCCESS(f"Importing data from {file_path}..."))
        df = pd.read_csv(file_path)
        collection.insert_many(df.to_dict(orient='records'))
        self.stdout.write(self.style.SUCCESS("Data imported successfully."))