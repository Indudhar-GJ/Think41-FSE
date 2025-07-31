import csv
from django.core.management.base import BaseCommand
from products.models import (
    Product, Department, Category, Brand, DistributionCenter
)


class Command(BaseCommand):
    help = 'Imports products from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)

            # Convert fieldnames to lowercase for case-insensitive matching
            reader.fieldnames = [name.strip().lower()
                                 for name in reader.fieldnames]
            i = 0
            for row in reader:
                try:
                    print("added row ", i)
                    i += 1
                    # Get or create related models with case-insensitive access
                    department, _ = Department.objects.get_or_create(
                        name=row.get('department', '').strip()
                    )
                    category, _ = Category.objects.get_or_create(
                        name=row.get('category', '').strip()
                    )
                    brand, _ = Brand.objects.get_or_create(
                        name=row.get('brand', '').strip()
                    )
                    distribution_center, _ = DistributionCenter.objects.get_or_create(
                        id=row.get('distribution_center_id', '').strip()
                    )

                    # Create product
                    Product.objects.update_or_create(
                        id=row.get('id'),
                        defaults={
                            'sku': row.get('sku', '').strip(),
                            'name': row.get('name', '').strip(),
                            'cost': float(row.get('cost', 0)),
                            'retail_price': float(row.get('retail_price', 0)),
                            'department': department,
                            'category': category,
                            'brand': brand,
                            'distribution_center': distribution_center,
                        }
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"Error processing row: {row}. Error: {str(e)}"))
                    continue

        self.stdout.write(self.style.SUCCESS('Successfully imported products'))
