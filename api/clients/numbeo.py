import unicodedata
from typing import Any
from typing import Tuple
from urllib.request import urlopen as uReq

from bs4 import BeautifulSoup as soup
from unidecode import unidecode


def _get_soup_page(city: str) -> soup:
    """Get the soup page object from numbeo.com for a given city."""
    req_url = f"https://www.numbeo.com/cost-of-living/in/{unidecode(city)}?displayCurrency=EUR"

    # opening connection, grabbing page
    uClient = uReq(req_url)
    page_html = uClient.read()
    uClient.close()

    # html parsing
    return soup(page_html, "html.parser")


def get_soup_page(city: str, alt: str) -> Tuple[Any, Any]:
    """Get the soup page object for either city, or the alternate entry if the first one fails."""
    page_soup = _get_soup_page(city)
    error = page_soup.findAll("div", style="error_message")
    if error:
        page_soup = _get_soup_page(alt)
        error = page_soup.findAll("div", style="error_message")
        if error:
            return [], error
    else:
        return page_soup.findAll("tr"), []
    return page_soup.findAll("tr"), []


def get_value(obj: Any, alt: Any) -> Any:
    if not obj:
        if not alt:
            return None
        else:
            return alt
    return obj


# extract costs from each row in each category
def get_costs(cost_rows_html: list) -> list:
    """This function extracts costs as floats from
    the html rows for each category."""
    costs = []
    for _, row in enumerate(cost_rows_html):
        c = row.find("td", class_="priceValue")
        c2 = row.find("td", class_="priceVaue tr_highlighted")

        t = row.find("td")
        t2 = row.find("td", class_="tr_highlighted")

        cost = get_value(c, c2)
        title = get_value(t, t2)
        if not cost:
            continue

        cost = cost.text.replace("\xa0", unicodedata.normalize("NFKC", "\xa0"))
        title = title.text.replace("\xa0", unicodedata.normalize("NFKC", "\xa0"))

        cost = cost.replace(",", "")
        title = title.replace(",", "")

        cost = cost.strip(" €")
        try:
            cost = float(cost)
        except ValueError:
            cost = None
        title = str(title)

        costs.append(
            {
                "sub_category": title,
                "cost": cost,
                "currency": "EUR",
            }
        )

    return costs


def process_country_city(country: str, city: str) -> dict:
    """This function processes the country and city and returns
    the cost of living by category, as scraped from Numbeo."""
    all_rows_html, err = get_soup_page(
        city.title().replace(" ", "-"),
        f"{city.title().replace(' ', '-')}-{country.title().replace(' ', '-')}",
    )
    if err:
        return err

    # select rows for each category
    restaurant_cost_rows_html = all_rows_html[2:10]
    market_cost_rows_html = all_rows_html[11:30]
    transportation_cost_rows_html = all_rows_html[31:39]
    utilities_cost_rows_html = all_rows_html[40:43]
    leisure_cost_rows_html = all_rows_html[44:47]
    # TODO: check what's in 45-46
    clothing_cost_rows_html = all_rows_html[51:55]
    rent_cost_rows_html = all_rows_html[56:60]

    # get lists of costs for each category
    restaurant_data = get_costs(restaurant_cost_rows_html)
    market_data = get_costs(market_cost_rows_html)
    transportation_data = get_costs(transportation_cost_rows_html)
    utilities_data = get_costs(utilities_cost_rows_html)
    leisure_data = get_costs(leisure_cost_rows_html)
    clothing_data = get_costs(clothing_cost_rows_html)
    rent_data = get_costs(rent_cost_rows_html)

    category_data = {
        "restaurant": restaurant_data,
        "market": market_data,
        "transportation": transportation_data,
        "utilities": utilities_data,
        "leisure": leisure_data,
        "clothing": clothing_data,
        "rent": rent_data,
    }

    return category_data
