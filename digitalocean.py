from requests_html import HTMLSession
from parsel import Selector
import pandas as pd
import re


def string_formatter(text, param):
    """Removes unnecessary texts from strings"""
    there = re.compile(re.escape(param) + '.*')
    return there.sub('', text)


# requesting webpage
s = HTMLSession()
url = "https://www.digitalocean.com/pricing"
r = s.get(url)
script = """
() => {
    function clickButton () {
    const item = document.querySelector("#__next > section > div.ContainerStyles__StyledContainer-sc-1vejnbq-0.fTRAxt.container > div.MasonryStyles__MasonryDiv-sc-n3swdp-0.cevqpZ > div:nth-child(1) > div:nth-child(1)");
    if(item) {
        item.click()
        }
    }
    clickButton();
}
"""
r.html.render(sleep=1, timeout=5000, script=script)
html_text = Selector(text=r.html.html)
r.close()

# columns
prices_column = html_text.xpath('//div[@class="HeroPricingStyles__StyledCost-sc-h8uh2t-30 phzTR"]//h2//text()').getall()
prices_column = prices_column[::2] # dropping '/mo/ values
memories_column = html_text.xpath('//h6[@class="HeadingStyles__StyledH6-sc-kkk1io-5 gzHKJA HeroPricing___StyledHeading4-sc-13g3nko-3 ghlWhj"]//text()').getall()
vcpus_column = html_text.xpath('//h6[@class="HeadingStyles__StyledH6-sc-kkk1io-5 gzHKJA HeroPricing___StyledHeading6-sc-13g3nko-5 ckBDHT"]//text()').getall()
vcpus_column = [string_formatter(i, 'Intel') for i in vcpus_column]
ssds_column = html_text.xpath('//h6[@class="HeadingStyles__StyledH6-sc-kkk1io-5 gzHKJA HeroPricing___StyledHeading8-sc-13g3nko-7 gAtIHP"]//text()').getall()
ssds_column = [string_formatter(i, ' ') for i in ssds_column]
transfer_column = html_text.xpath('//h6[@class="HeadingStyles__StyledH6-sc-kkk1io-5 gzHKJA HeroPricing___StyledHeading10-sc-13g3nko-9 ifDSDM"]//text()').getall()

data_dict = {
    'Memory': memories_column,
    'vCPUs': vcpus_column,
    'Transfer': transfer_column,
    'SSD': ssds_column,
    'Price[$/mo]': prices_column
}

do_df = pd.DataFrame(data_dict)

crawler_execution_text = """Crawler executado com sucesso.
O que deseja fazer?
--print
--save_csv
--save_json
Digite a opção desejada: """

if r.ok: # checks if http response == 200
    answer = input(crawler_execution_text)
    if answer == "--print":
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(do_df)
    elif answer == "--save_csv":
        do_df.to_csv('digitalocean.csv', index=False)
    elif answer == "--save_json":
        do_df.to_json('digitalocean.json', orient="table")
    else:
        print("Resposta inválida")
else:
    print('Página indisponível no momento.')

