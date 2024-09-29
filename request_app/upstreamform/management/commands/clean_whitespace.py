from django.core.management.base import BaseCommand
from upstreamform.models import ChargingList

class Command(BaseCommand):
    help = 'Removes leading and trailing spaces from all fields in ChargingList model'

    def handle(self, *args, **kwargs):
        records = ChargingList.objects.all()
        count = 0

        for record in records:
            fields_to_clean = [
                'state', 'category', 'base_fare', 'flat_fee', 'free_for', 
                'per_page', 'fee_limit', 'fee_limit_for_mail', 
                'fee_limit_for_electronic', 'page_1', 'page_1_to_5', 
                'page_1_to_10', 'page_1_to_20', 'page_1_to_25', 
                'page_1_to_30', 'page_1_to_40', 'page_1_to_50', 
                'page_1_to_80', 'page_1_to_100', 'page_1_to_150', 
                'page_1_to_250', 'page_1_to_1000', 'page_2_to_30', 
                'page_2_to_200', 'page_11_to_20', 'page_11_to_40', 
                'page_11_to_50', 'page_21_to_30', 'page_21_to_40', 
                'page_21_to_50', 'page_21_to_60', 'page_21_to_100', 
                'page_21_to_500', 'page_26_to_100', 'page_26_to_350', 
                'page_31_to_100', 'page_101_to_200', 'above_5_pages', 
                'above_10_pages', 'above_20_pages', 'above_25_pages', 
                'above_30_pages', 'above_40_pages', 'above_50_pages', 
                'above_60_pages', 'above_80_pages', 'above_100_pages', 
                'above_150_pages', 'above_200_pages', 'above_250_pages', 
                'above_350_pages', 'above_500_pages', 'above_1000_pages', 
                'first_hour', 'each_additional_hour', 'required_fee', 
                'amount', 'optional_fee', 'amount_1', 'optional_fee_1', 
                'amount_2'
            ]

            updated = False
            for field in fields_to_clean:
                value = getattr(record, field, None)
                if value and isinstance(value, str):
                    cleaned_value = value.strip()
                    if cleaned_value != value:
                        setattr(record, field, cleaned_value)
                        updated = True

            if updated:
                record.save()
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully cleaned {count} records'))
