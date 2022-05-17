"""
Project OpenClassRooms n°2 : Uses bases of Python for market analysis
"""

from itertools import product
import requests
from bs4 import BeautifulSoup

import csv


"""
Step 1 : Écrivez un script Python qui visite cette page et en extrait les informations suivantes
"""


"""Initialization of a BeautifulSoup object"""
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
HTML_web_page = requests.get(url)
soup = BeautifulSoup(HTML_web_page.content, "html.parser")

review_rating_string_int_correspondance = {
    "One" : 1,
    "Two" : 2,
    "Three" : 3,
    "Four" : 4,
    "Five": 5
}


product_page_urls_list = []
universal_product_codes_list = []
titles_list = []
prices_including_tax_list = []
prices_excluding_tax_list = []
numbers_available_list = []
products_descriptions_list = []
categories_list = []
review_ratings_list = []
images_urls_list = []

def information_extraction():
    """Extraction of information asked by the step 1 of the OpenClassRoom project"""




    #Product information table
    product_information_table = soup.find(class_ = "table table-striped")
    product_information = product_information_table.find_all("td")

    #URL
    product_page_url = HTML_web_page.url
    product_page_urls_list.append(product_page_url)

    #UPC
    universal_product_code = product_information[0].string
    universal_product_codes_list.append(universal_product_code)

    #Title
    title = soup.find(class_ = "active").string
    titles_list.append(title)

    #Prices
    price_including_tax = product_information[3].string
    prices_including_tax_list.append(price_including_tax)

    price_excluding_tax = product_information[2].string
    prices_excluding_tax_list.append(price_excluding_tax)

    #Availability
    availability = product_information[5].string
    if "In stock" in availability:
        number_available = availability[10:-11]
    else:
        number_available = "No available"
    numbers_available_list.append(number_available)

    #Product description
    product_description_title = soup.find(id = "product_description")
    product_description = product_description_title.find_next_sibling("p").string
    products_descriptions_list.append(product_description)

    #Category
    breadcrumb_class = soup.find(class_="breadcrumb")
    breadcrumb_class_lis = breadcrumb_class.findAll("li")
    breadcrumb_class_lis_a = breadcrumb_class_lis[2]
    category = breadcrumb_class_lis_a.find("a").string
    categories_list.append(category)

    #Review rating
    #NB: i tried with """ print(paragraph["class_"]) """" : key error
    paragraphs_attributes = []
    paragraphs = soup.findAll("p")
    for paragraph in paragraphs:
        paragraphs_attributes.append(paragraph.attrs)
    for paragraphs_attribute in paragraphs_attributes:
        for key in paragraphs_attribute:
            if key == "class":
                if paragraphs_attribute[key][0] == "star-rating":
                    review_rating_string = paragraphs_attribute[key][1]
    review_rating = review_rating_string_int_correspondance[review_rating_string]
    review_ratings_list.append(review_rating)

    #Image URL
    item_active = soup.find(class_ ="item active")
    image = item_active.find("img") 
    image_url = "http://books.toscrape.com" + image["src"][5:]
    images_urls_list.append(image_url)    

    #TEST
    print("product_page_url", product_page_url)
    print("")
    print("universal_product_code", universal_product_code)
    print("")
    print("title", title)
    print("")
    print("price_including_tax", price_including_tax)
    print("")
    print("price_excluding_tax", price_excluding_tax)
    print("")
    print("number_available", number_available)
    print("")
    print("product_description", product_description)
    print("")
    print("category", category)
    print("")
    print("review_rating", review_rating)
    print("")
    print("image_url", image_url)



"""STEP 2 : Écrivez les données dans un fichier CSV qui utilise les champs ci-dessus comme en-têtes de colonnes."""
def information_csv_loading():
    table_headers = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]

    #new file creation
    with open('books_toscrap.csv', 'w') as csv_file:
    
    #creation of a 'writer' object
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(table_headers)

        for product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url in zip(product_page_urls_list, universal_product_codes_list, titles_list, prices_including_tax_list, prices_excluding_tax_list, numbers_available_list, products_descriptions_list, categories_list, review_ratings_list, images_urls_list) :
            line = [product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url]
            csv_writer.writerow(line)

def main():
    information_extraction()
    information_csv_loading()

main()



"""
fichier = open("hello.txt", "w")
with open("file.txt") as fichier:#mode douverture par defaut : r
"""
