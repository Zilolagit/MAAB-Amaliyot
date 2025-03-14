from random import randint

import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import random

def scrape_golden_pages():
    url = "https://www.goldenpages.uz/en/"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve page")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    containers = soup.find_all("div", class_="mainContainer")

    links = []
    for container in containers:
        category_lists = container.find_all("ul", class_="gp_list_category")

        for category_list in category_lists:
            all_links = category_list.find_all("a")

            for link in all_links:
                links.append(link.text.strip()[:12])


    top_20_categories = links[:20]
    top_20_companies = links[20:40]
    top_20_comp_site = links[40:60]
    top_20_comp_map = links[60:80]


    categories_counts_1 = [random.randint(1, 20) for _ in range(1, 6)]
    categories_counts_2 = [random.randint(1, 20) for _ in range(1, 6)]
    categories_counts_3 = [random.randint(1, 20) for _ in range(1, 6)]
    categories_counts_4 = [random.randint(1, 20) for _ in range(1, 6)]


    def figure(text, list_val):
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(text, fontsize=16, fontweight='bold')

        # First Subplot
        axes[0, 0].plot(list_val[:5], categories_counts_1, color="skyblue")

        # Second Subplot
        axes[0, 1].plot(list_val[5:10], categories_counts_2, color="skyblue")

        # Third Subplot
        axes[1, 0].plot(list_val[10:15], categories_counts_3, color="skyblue")

        # Fourth Subplot
        axes[1, 1].plot(list_val[15:20], categories_counts_4, color="skyblue")

    figure("TOP 20 Categories for February", top_20_categories)
    figure("TOP 20 most popular companies for February", top_20_companies)
    figure("New 20 companies on site", top_20_comp_site)
    figure("New 20 companies on map", top_20_comp_map)

    plt.show()

scrape_golden_pages()
