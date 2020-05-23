import os
import csv
from decimal import Decimal

from django.conf import settings
from django.shortcuts import render


class PhoneMastData:
    def __init__(self, csv_file=None):
        self.file_name = csv_file

    def read_csv(self):
        properties = []

        try:
            with open(self.file_name) as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    properties.append(row)
        except FileNotFoundError:
            print('File not found.')
            # We just return an empty list if file not found. We don't want to stop the app from working.
            # and silent raise the error - in this case just a standard print to the console.
            pass

        return properties

    def sort_current_rent(self):
        property_data = self.read_csv()
        property_data = sorted(property_data, key=lambda x: Decimal(x.get('Current Rent')))

        # Print first 5 items to console
        print(property_data[:5])
        return property_data


def get_operation(request):
    """
    Allows the user to select what operation they want to run.
    """
    return render(request, 'index.html')


def sort_by_current_rent(request):
    """
    Sorts the data by 'Current Rent' in Ascending order.
    """
    file_path = os.path.join(settings.BASE_DIR, 'phone_mast/test_data/may2020_test_data.csv')
    phone_mast_data = PhoneMastData(csv_file=file_path)
    data = phone_mast_data.sort_current_rent()

    return render(
        request,
        'index.html',
        {'property_data': data}
    )
