import csv
import os
from decimal import Decimal

import pytest

from phone_mast.views import PhoneMastData, read_csv
from phone_mast.exceptions import InvalidDateFormat


@pytest.fixture
def phone_mast_data_csv():
    with open('test.csv', 'w') as csv_file:
        fieldnames = [
            'Property Name',
            'Property Address [1]',
            'Property  Address [2]',
            'Property Address [3]',
            'Property Address [4]',
            'Unit Name',
            'Tenant Name',
            'Lease Start Date',
            'Lease End Date',
            'Lease Years',
            'Current Rent',
        ]
        data_rows = [
            {
                'Property Name': 'Beecroft Hill',
                'Property Address [1]': 'Broad Lane',
                'Property  Address [2]': '',
                'Property Address [3]': '',
                'Property Address [4]': 'LS13',
                'Unit Name': 'Beecroft Hill - Telecom App',
                'Tenant Name': 'Arqiva Services ltd',
                'Lease Start Date': '01 Mar 1994',
                'Lease End Date': '28 Feb 2058',
                'Lease Years': '64',
                'Current Rent': '23950.00'
            },
            {
                'Property Name': 'Potternewton Crescent',
                'Property Address [1]': 'Potternewton Est Playing Field',
                'Property  Address [2]': '',
                'Property Address [3]': '',
                'Property Address [4]': 'LS7',
                'Unit Name': 'Potternewton Est Playing Field',
                'Tenant Name': 'Arqiva Ltd',
                'Lease Start Date': '24 Jun 1999',
                'Lease End Date': '23 Jun 2019',
                'Lease Years': '20',
                'Current Rent': '6600.00'
            },
            {
                'Property Name': 'Seacroft Gate (Chase) - Block 2',
                'Property Address [1]': 'Telecomms Apparatus',
                'Property  Address [2]': 'Leeds',
                'Property Address [3]': '',
                'Property Address [4]': 'LS14',
                'Unit Name': 'Seacroft Gate (Chase) block 2-Telecom App.',
                'Tenant Name': 'Vodafone Ltd.',
                'Lease Start Date': '30 Jan 2004',
                'Lease End Date': '29 Jan 2029',
                'Lease Years': '25',
                'Current Rent': '12250.00'
            },
            {
                'Property Name': 'Queenswood Heights',
                'Property Address [1]': 'Queenswood Heights',
                'Property  Address [2]': 'Queenswood Gardens',
                'Property Address [3]': 'Headingley',
                'Property Address [4]': 'Leeds',
                'Unit Name': 'Queenswood Hgt-Telecom App.',
                'Tenant Name': 'Vodafone Ltd',
                'Lease Start Date': '08 Nov 2004',
                'Lease End Date': '07 Nov 2029',
                'Lease Years': '25',
                'Current Rent': '9500.00'
            },
            {
                'Property Name': 'Norman Towers (Telecom Appar)',
                'Property Address [1]': 'Spen Lane',
                'Property  Address [2]': 'Leeds',
                'Property Address [3]': '',
                'Property Address [4]': 'LS16',
                'Unit Name': 'Norman Towers (Telecom Appar) 1701o2',
                'Tenant Name': 'Cornerstone Telecommunications Infrastructure',
                'Lease Start Date': '31 Mar 2015',
                'Lease End Date': '30 Mar 2030',
                'Lease Years': '15',
                'Current Rent': '22500.00'
            },
            {
                'Property Name': 'King Lane',
                'Property Address [1]': 'Leafield Towers',
                'Property  Address [2]': 'Leeds',
                'Property Address [3]': '',
                'Property Address [4]': 'LS16',
                'Unit Name': 'Leafield Towers - Cell 5516vf',
                'Tenant Name': 'Cornerstone Telecommunications Infrastructure',
                'Lease Start Date': '31 Mar 2015',
                'Lease End Date': '30 Mar 2030',
                'Lease Years': '15',
                'Current Rent': '15000.00'
            }
        ]

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_rows:
            writer.writerow(data)

        data_file = csv_file

    return data_file


def test_read_csv(phone_mast_data_csv):
    result = read_csv(file_name='test.csv')
    os.remove('test.csv')

    assert len(result) > 0


def test_sort_by_current_rent(phone_mast_data_csv):
    phone_mast = PhoneMastData(csv_file='test.csv')
    result = phone_mast.sort_current_rent()
    os.remove('test.csv')

    assert len(result) > 0
    assert Decimal(result[0]['Current Rent']) == Decimal(6600)
    assert Decimal(result[-1]['Current Rent']) == Decimal(23950)


def test_filter_by_lease(phone_mast_data_csv):
    phone_mast = PhoneMastData(csv_file='test.csv')
    result = phone_mast.filter_by_lease_years(25)
    os.remove('test.csv')

    assert len(result[0]) == 2
    assert result[1] == Decimal('21750.00')


def test_tenant_mast_count(phone_mast_data_csv):
    phone_mast = PhoneMastData(csv_file='test.csv')
    result = phone_mast.count_mast_by_tenant()
    os.remove('test.csv')

    assert len(result) == 5
    assert result['Arqiva Ltd'] == 1
    assert result['Cornerstone Telecommunications Infrastructure'] == 2


def test_filter_by_lease_start_date(phone_mast_data_csv):
    phone_mast = PhoneMastData(csv_file='test.csv')
    result = phone_mast.filter_by_lease_start_date('1999-06-01', '2001-07-31')
    os.remove('test.csv')

    assert len(result) == 1
    assert result[0]['Lease Start Date'] == '24/06/1999'


# ------ Error Tests ------


def test_no_csv_file():
    result = read_csv(file_name='no_file.csv')

    assert len(result) == 0


def test_filter_by_lease_start_date_invalid_formate(phone_mast_data_csv):
    phone_mast = PhoneMastData(csv_file='test.csv')
    with pytest.raises(InvalidDateFormat):
        os.remove('test.csv')
        result = phone_mast.filter_by_lease_start_date('06-01-1999', '2001-07-31')
        