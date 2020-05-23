import os
import csv
from datetime import datetime
from decimal import Decimal
from pprint import pprint

from django.conf import settings
from django.shortcuts import render
from django.views import View


def read_csv(file_name=None):
    properties = []

    try:
        with open(file_name) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                properties.append(row)
    except FileNotFoundError:
        print('File not found.')
        # We just return an empty list if file not found. We don't want to stop the app from working.
        # and silent raise the error - in this case just a standard print to the console.
        pass

    return properties


class PhoneMastData:
    def __init__(self, csv_file=None):
        self.data_file = read_csv(csv_file)

    def sort_current_rent(self):
        property_data = self.data_file
        property_data = sorted(property_data, key=lambda x: Decimal(x.get('Current Rent')))

        # Print first 5 items to console
        print(property_data[:5])
        return property_data

    def filter_by_lease_years(self, lease_year: int):
        property_data = self.data_file
        filtered_data = [data for data in property_data if int(data['Lease Years']) == lease_year]
        total_rent = sum([Decimal(rent['Current Rent']) for rent in filtered_data])

        print(filtered_data)
        print(f'Total rent: {total_rent}')
        return [filtered_data, total_rent]

    def count_mast_by_tenant(self):
        property_data = self.data_file
        tenants = {}

        for data in property_data:
            if tenants.get(data['Tenant Name']):
                tenants[data['Tenant Name']] += 1
            else:
                tenants[data['Tenant Name']] = 1

        pprint(tenants)
        return tenants

    def filter_by_lease_start_date(self, start_date: str, end_date: str):
        property_data = self.data_file
        for data in property_data:
            data['Lease Start Date'] = datetime.strptime(data['Lease Start Date'], '%d %b %Y')

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        filtered_data_by_date = [
            data for data in property_data if start_date < data['Lease Start Date'] < end_date
        ]

        for dates in filtered_data_by_date:
            dates['Lease Start Date'] = dates['Lease Start Date'].strftime('%d/%m/%Y')

        pprint(filtered_data_by_date)
        return filtered_data_by_date


def get_operation(request):
    """
    Allows the user to select what operation they want to run.
    """
    if request.method == 'GET':
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


def filter_by_lease(request):
    """
    Filter data by lease and calculates toatal rent for given lease year.
    """
    file_path = os.path.join(settings.BASE_DIR, 'phone_mast/test_data/may2020_test_data.csv')
    phone_mast_data = PhoneMastData(csv_file=file_path)
    data, rent = phone_mast_data.filter_by_lease_years(25)

    return render(
        request,
        'index.html',
        {'property_data': data}
    )


def tenant_count(request):
    """
    Count mast by tenants.
    """
    file_path = os.path.join(settings.BASE_DIR, 'phone_mast/test_data/may2020_test_data.csv')
    phone_mast_data = PhoneMastData(csv_file=file_path)
    data = phone_mast_data.count_mast_by_tenant()

    return render(
        request,
        'index.html',
        {'property_data': data}
    )


def filter_lease_date(request):
    """
    Count mast by tenants.
    """
    file_path = os.path.join(settings.BASE_DIR, 'phone_mast/test_data/may2020_test_data.csv')
    phone_mast_data = PhoneMastData(csv_file=file_path)
    data = phone_mast_data.filter_by_lease_start_date('1999-06-01', '2001-07-31')

    return render(
        request,
        'index.html',
        {'property_data': data}
    )

