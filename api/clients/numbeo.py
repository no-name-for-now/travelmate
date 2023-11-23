import unicodedata
from typing import Any
from typing import Tuple
from urllib.request import urlopen as uReq

from bs4 import BeautifulSoup as soup
from unidecode import unidecode


categories = [
    "restaurants",
    "markets",
    "transportation",
    "utilities",
    "leisure",
    "clothing",
    "rent",
]


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
        title = str(title)

        try:
            cost = float(cost)
            costs.append(
                {
                    "sub_category": title,
                    "cost": cost,
                    "currency": "EUR",
                }
            )

        except ValueError:
            continue
    return costs


def process_country_city(country: str, city: str) -> list[dict[str, Any]]:
    """This function processes the country and city and returns
    the cost of living by category, as scraped from Numbeo."""
    all_rows_html, err = get_soup_page(
        city=city.title().replace(" ", "-"),
        alt=f"{city.title().replace(' ', '-')}-{country.title().replace(' ', '-')}",
    )
    if err:
        raise Exception(err)

    restaurants_cost_rows_html = all_rows_html[2:10]  # noqa: F841
    markets_cost_rows_html = all_rows_html[11:30]  # noqa: F841
    transportation_cost_rows_html = all_rows_html[31:39]  # noqa: F841
    utilities_cost_rows_html = all_rows_html[40:43]  # noqa: F841
    leisure_cost_rows_html = all_rows_html[44:47]  # noqa: F841
    clothing_cost_rows_html = all_rows_html[51:55]  # noqa: F841
    rent_cost_rows_html = all_rows_html[56:60]  # noqa: F841

    # get list of costs for each category
    category_data = []
    for category in categories:
        cost_data = get_costs(eval(f"{category}_cost_rows_html"))
        for cost_row in cost_data:
            category_data.append(
                {
                    "city": city,
                    "category": category,
                    "sub_category": cost_row["sub_category"],
                    "cost": cost_row["cost"],
                    "currency": cost_row["currency"],
                }
            )

    return category_data
