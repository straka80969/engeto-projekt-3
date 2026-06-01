"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: David Straka
email: Strak80969@mot.sps-dopravni.cz
discord: -
"""

import sys
import csv
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.volby.cz/pls/ps2017nss/"


def get_soup(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "html.parser")


def validate_url(url):
    return "volby.cz/pls/ps2017nss/" in url


def parse_municipalities(url):
    soup = get_soup(url)

    municipalities = []
    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 3:
                link = row.find("a")
                if link and "ps311" in link.get("href", ""):
                    code = cells[0].get_text(strip=True)
                    name = cells[1].get_text(strip=True)
                    detail_url = BASE_URL + link["href"]
                    municipalities.append((code, name, detail_url))

    return municipalities


def parse_municipality(detail_url):
    soup = get_soup(detail_url)

    voters = soup.find("td", headers="sa2").get_text(strip=True).replace("\xa0", "")
    envelopes = soup.find("td", headers="sa3").get_text(strip=True).replace("\xa0", "")
    valid_votes = soup.find("td", headers="sa6").get_text(strip=True).replace("\xa0", "")

    parties = {}
    for row in soup.find_all("tr"):
        party = row.find("td", headers="t1sa1")
        votes = row.find("td", headers="t1sa2")

        if party and votes:
            parties[party.get_text(strip=True)] = votes.get_text(strip=True).replace("\xa0", "")

        party = row.find("td", headers="t2sa1")
        votes = row.find("td", headers="t2sa2")

        if party and votes:
            parties[party.get_text(strip=True)] = votes.get_text(strip=True).replace("\xa0", "")

    return voters, envelopes, valid_votes, parties


def main():
    if len(sys.argv) != 3:
        print("Použití: python projekt_3.py <url> <vystup.csv>")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    if not validate_url(url):
        print("Neplatný odkaz.")
        sys.exit(1)

    municipalities = parse_municipalities(url)

    if not municipalities:
        print("Nepodařilo se načíst data.")
        sys.exit(1)

    all_parties = []
    rows = []

    for code, name, detail_url in municipalities:
        voters, envelopes, valid_votes, parties = parse_municipality(detail_url)

        for party in parties:
            if party not in all_parties:
                all_parties.append(party)

        rows.append({
            "code": code,
            "name": name,
            "voters": voters,
            "envelopes": envelopes,
            "valid_votes": valid_votes,
            "parties": parties
        })

    with open(output_file, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        header = [
            "code",
            "location",
            "registered",
            "envelopes",
            "valid"
        ] + all_parties

        writer.writerow(header)

        for row in rows:
            data = [
                row["code"],
                row["name"],
                row["voters"],
                row["envelopes"],
                row["valid_votes"]
            ]

            for party in all_parties:
                data.append(row["parties"].get(party, "0"))

            writer.writerow(data)

    print(f"Uloženo do souboru: {output_file}")


if __name__ == "__main__":
    main()
