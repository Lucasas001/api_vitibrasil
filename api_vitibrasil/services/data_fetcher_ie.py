# Author: Lucas Martins

import requests
import time
import logging
from bs4 import BeautifulSoup


def remove_dot_for_int_value(column: str):
    try:
        number = float(column)
        if number.is_integer():
            return str(int(number))
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

    for row in tbody.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) >= 3:
            country = cols[0].get_text(strip=True)
            quantity = cols[1].get_text(strip=True).replace("-", "0")
            value = cols[2].get_text(strip=True).replace("-", "0")

            data.append(
                {
                    "paises": country,
                    "quantidade_kg": remove_dot_for_int_value(quantity),
                    "valor_us": remove_dot_for_int_value(value),
                }
            )

    tfoot = table.find("tfoot")
    if tfoot:
        total_row = tfoot.find("tr")
        if total_row:
            tds = total_row.find_all("td")
            if len(tds) >= 3:
                total_country = tds[0].get_text(strip=True)
                total_total_quantity = tds[1].get_text(strip=True)
                total_value = tds[2].get_text(strip=True)
                data.append(
                    {
                        "paises": total_country,
                        "quantidade_kg": remove_dot_for_int_value(total_total_quantity),
                        "valor_us": remove_dot_for_int_value(total_value),
                    }
                )
    else:
        data.append({"paises": "Total", "quantidade_kg": "0", "valor_us": "0"})

    return data


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def fetch_json_data_ie(url_base: str):
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
