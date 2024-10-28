# Author: Lucas Martins

import polars as pl
import requests
import time
import logging
from bs4 import BeautifulSoup


def remove_dot_for_int_value(column: str):
    try:
        number = float(column)
        if number.is_integer():
            return str(column).replace(".", "")
        else:
            return str(column)
    except ValueError:
        return column


def content_parser(response):
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"class": "tb_base tb_dados"})
    if not table:
        return [{"error": "Table not found in HTML content"}]

    tbody = table.find("tbody")
    if not tbody:
        return [{"error": "Table body (tbody) not found"}]

    data = []
    current_item = None

    for row in tbody.find_all("tr"):
        cols = row.find_all("td")
        if not cols:
            continue
        first_td = cols[0]
        item_classes = first_td.get("class", [])
        item_type = item_classes[0] if item_classes else None

        if item_type == "tb_item":
            current_item = first_td.get_text(strip=True)
            current_value = cols[1].get_text(strip=True) if len(cols) > 1 else None
            data.append(
                {
                    "item": current_item,
                    "subitem": current_item,
                    "value": remove_dot_for_int_value(current_value),
                }
            )
        elif item_type == "tb_subitem" and current_item:
            subitem = first_td.get_text(strip=True)
            sub_value = cols[1].get_text(strip=True) if len(cols) > 1 else None
            data.append(
                {
                    "item": current_item,
                    "subitem": subitem,
                    "value": remove_dot_for_int_value(sub_value),
                }
            )

    tfoot = table.find("tfoot")
    if tfoot:
        total_row = tfoot.find("tr")
        if total_row:
            tds = total_row.find_all("td")
            if len(tds) >= 2:
                total_item = tds[0].get_text(strip=True)
                total_value = tds[1].get_text(strip=True)
                data.append(
                    {
                        "item": total_item,
                        "subitem": None,
                        "value": remove_dot_for_int_value(total_value),
                    }
                )
    else:
        data.append({"item": "Total", "subitem": None, "value": "Unavailable"})

    return data


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def fetch_json_data(url_base: str):
    max_attempts = 3
    attempts = 0
    wait_time = 5
    response = None

    while attempts < max_attempts:
        try:
            logging.info(f"Attempt {attempts + 1} to connect to the server.")
            response = requests.get(url_base)
            response.raise_for_status()
            logging.info("Successfully connected to the server.")
            return response.status_code, content_parser(response)

        except requests.exceptions.RequestException as e:
            attempts += 1
            logging.error(f"Error on attempt {attempts} of {max_attempts}. Error: {e}")
            if attempts == max_attempts:
                logging.critical(
                    f"Failed to retrieve data after {max_attempts} attempts."
                )
                return response.status_code if response else None, [
                    {
                        "error": f"Failed to retrieve data after {max_attempts} attempts: {e}"
                    }
                ]
            else:
                logging.info(f"Waiting {wait_time} seconds before the next attempt.")
                time.sleep(wait_time)


# if __name__ == "__main__":
#     url_base = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2010&opcao=opt_03&subopcao=subopt_01"
#
#     status_code, current_data = fetch_json_data(url_base=url_base)
#     pprint.pprint((current_data))
#
#     df = pl.DataFrame(current_data)
#     print(df)
