import requests
import csv
from bs4 import BeautifulSoup


def get_urls(save_to_file = False):
    URL = "https://distrowatch.com/search.php?status=All"
    response = requests.get(URL)

    html_doc = response.content

    soup = BeautifulSoup(html_doc, "lxml")

    b_tags = soup.find_all("td", class_="NewsText")

    URL_list = []
    for a_tag in b_tags[1].find_all("a", href=True):
        URL_list.append("https://distrowatch.com/" + a_tag["href"])

    if save_to_file is True:
        with open('urls.txt', 'w') as f:
            for line in URL_list[3:]:
                f.write(f"{line}\n")

    return URL_list

def get_distro_list():
    distro_URL = get_urls()[3]
    distro_list = []
    for distro_URL in get_urls()[3:]:
        distro = {}
        distro_response = requests.get(distro_URL)
        distro_soup = BeautifulSoup(distro_response.content, "lxml")

        name_row = distro_soup.find("th", string="Distribution")
        distro_name = name_row.next_sibling.next_sibling.get_text()
        distro['distro_name'] = distro_name

        web_row = distro_soup.find("th", string="Home Page")
        distro_web = web_row.next_sibling.next_sibling.get_text()
        distro['distro_web'] = distro_web

        download_row = distro_soup.find("th", string="Download Mirrors")
        distro_download = download_row.next_sibling.next_sibling.a.get_text()
        distro['distro_download'] = distro_download

        based_on = distro_soup.find("b", string="Based on:").parent.find_all("a")
        bases = []
        for base in based_on:
            bases.append(base.get_text())
        distro['based_on'] = bases
        
        desktops = distro_soup.find("b", string="Desktop:").parent.find_all("a")
        desktop_names = []
        for desktop in desktops:
            desktop_names.append(desktop.get_text())
        distro['desktop_names'] = desktop_names
        
        description = distro_soup.find("td", class_="TablesTitle").contents[10]
        distro['description'] = description

        print(distro)
        distro_list.append(distro)
    return distro_list

get_distro_list()