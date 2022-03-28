import re
import requests
import pandas as pd
from parsel import Selector
from collections import OrderedDict


def list_cleaner(item):
    """"Removes special characters and blank spaces from a list of strings"""
    cleaned_item = re.sub('\n|\t', '', item).strip()
    return cleaned_item


def to_matrix(list, n):
    """Transforms one dimension lists into two dimension lists"""
    return [list[i:i+n] for i in range(0, len(list), n)]


# requesting webpage
r = requests.get('https://www.vultr.com/products/cloud-compute/#pricing')

if r.ok: # checking if http response == 200
    html_text = Selector(text=r.text)
    # clicking on the link that redirects to the page where prices are
    domain = 'https://www.vultr.com'
    prices_page = html_text.xpath(
        '//a[@class="btn btn--lg btn--light-overlay btn--outline"]//@href').get()
    r = requests.get(f'{domain}{prices_page}')
    # turns the webpage in text
    html_text = Selector(text=r.text)

    # crawling types and subtypes
    types = html_text.xpath('//div[@id="cloud-compute"]//h3[@class="pricing__subsection-title"]//text()').getall()
    types = [list_cleaner(i) for i in types]
    types = list(filter(None, types))  # removing empty items
    subtypes = html_text.xpath('//div[@class="pricing__subsection"]//h4//text()').getall()

    # crawling columns_names
    columns_names = html_text.xpath('//div[@class="pt__cell"]//text()').getall()
    columns_names = [list_cleaner(i) for i in columns_names]
    columns_names = list(filter(None, columns_names))  # removing empty items
    columns_names = list(OrderedDict.fromkeys(columns_names))

    # crawling rows
    cloud_compute_query = '//div[@id="cloud-compute"]//div[@class="pricing__subsection"]'

    high_performance_rows = html_text.xpath(f'{cloud_compute_query}[1]//strong//text()').getall()
    slicer = int((len(high_performance_rows) / 2))

    amd_rows = high_performance_rows[:slicer]
    amd_rows = [list_cleaner(i) for i in amd_rows]
    amd_rows_matrix = to_matrix(amd_rows, 6)

    intel_rows = high_performance_rows[slicer:]
    intel_rows = [list_cleaner(i) for i in intel_rows]
    intel_rows_matrix = to_matrix(intel_rows, 6)

    high_frequency_rows = html_text.xpath(f'{cloud_compute_query}[2]//strong//text()').getall()
    high_frequency_rows = [list_cleaner(i) for i in high_frequency_rows]
    high_frequency_rows_matrix = to_matrix(high_frequency_rows, 6)

    regular_performance_rows = html_text.xpath(f'{cloud_compute_query}[3]//strong//text()').getall()
    regular_performance_rows = [list_cleaner(i) for i in regular_performance_rows]
    regular_performance_rows_matrix = to_matrix(regular_performance_rows, 6)

    # making dataframes
    amd_df = pd.DataFrame.from_records(amd_rows_matrix, columns=columns_names)
    amd_df.insert(0, 'Type', types[0])
    amd_df.insert(1, 'Subtype', subtypes[0])

    intel_df = pd.DataFrame.from_records(intel_rows_matrix, columns=columns_names)
    intel_df.insert(0, 'Type', types[0])
    intel_df.insert(1, 'Subtype', subtypes[1])

    high_frequency_df = pd.DataFrame.from_records(high_frequency_rows_matrix, columns=columns_names)
    high_frequency_df.insert(0, 'Type', types[1])
    high_frequency_df.insert(1, 'Subtype', '')

    regular_performance_df = pd.DataFrame.from_records(regular_performance_rows_matrix, columns=columns_names)
    regular_performance_df.insert(0, 'Type', types[2])
    regular_performance_df.insert(1, 'Subtype', '')

    # concatenating all dfs
    vultr_df = pd.concat([amd_df, intel_df, high_frequency_df, regular_performance_df], ignore_index=True)
    vultr_df = vultr_df.iloc[:, :-1]  # dropping hourly price

else:
    print("Página indisponível no momento. Tente novamente mais tarde.")

