"""
OpenClassRooms Project n°2 : Uses bases of Python for market analysis
"""


from itertools import product
from os import link
from os import mkdir

import requests
from bs4 import BeautifulSoup

import csv


review_rating_string_int_correspondance = {
    "One" : 1,
    "Two" : 2,
    "Three" : 3,
    "Four" : 4,
    "Five": 5
}

def tables_for_product_information_extraction_initialization():
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
    
    return product_page_urls_list, universal_product_codes_list, titles_list, prices_including_tax_list, prices_excluding_tax_list, numbers_available_list, products_descriptions_list, categories_list, review_ratings_list, images_urls_list

def requests_web_page_product_initialization(url_product):
    """Initialization of a Requests object corresponding to a product (a book) web page"""

    requests_web_page_product = requests.get(url_product)

    return requests_web_page_product


def soup_product_initialization(requests_web_page_product):
    """Initialization of a BeautifulSoup object corresponding to a product (a book) web page"""

    soup_product = BeautifulSoup(requests_web_page_product.content, "html.parser")
    
    return soup_product


def soup_product_information_table_initialization(soup_product):
    """Initialization of the information table of the soup product"""
 
    product_information_table = soup_product.find(class_ = "table table-striped")
    product_information = product_information_table.find_all("td")

    return product_information 



def product_page_urls_list_extraction(requests_web_page_product, product_page_urls_list):
    """Returns product_page_url from HTML_web_page_product"""

    product_page_url = requests_web_page_product.url
    product_page_urls_list.append(product_page_url)

    return product_page_url


def universal_product_code_extraction(product_information, universal_product_codes_list):
    """Returns universal_product_code from product_information"""

    universal_product_code = product_information[0].string
    universal_product_codes_list.append(universal_product_code)

    return universal_product_code


def title_extraction(soup_product, titles_list):
    """Returns title from soup_product"""

    title = soup_product.find(class_ = "active").string
    titles_list.append(title)

    return title


def price_including_tax_extraction(product_information, prices_including_tax_list):
    """Returns price_including_tax from product_information"""

    price_including_tax = product_information[3].string
    prices_including_tax_list.append(price_including_tax)

    return price_including_tax


def price_excluding_tax_extraction(product_information, prices_excluding_tax_list):
    """Returns price_excluding_tax from product_information"""

    price_excluding_tax = product_information[2].string
    prices_excluding_tax_list.append(price_excluding_tax)

    return price_excluding_tax


def number_available_extraction(product_information, numbers_available_list):
    """Returns number_available from product_information"""

    availability = product_information[5].string
    if "In stock" in availability:
        number_available = availability[10:-11]
    else:
        number_available = "No available"
    numbers_available_list.append(number_available)

    return number_available


products_with_AttributeError_for_product_description_extraction = []


def product_description_extraction(soup_product, products_descriptions_list):
    """Returns product_description from soup_product"""

    global products_with_AttributeError_for_product_description_extraction

    #error with http://books.toscrape.com/catalogue/alice-in-wonderland-alices-adventures-in-wonderland-1_5/index.html
    try:
        product_description_title = soup_product.find(id = "product_description")
        product_description = product_description_title.find_next_sibling("p").string
    except AttributeError:
        product_description = ""
        
        products_with_AttributeError_for_product_description_extraction.append(soup_product.find(class_ = "active").string) #the name, but i do not use the function  title_extraction as it requires a table
        print("AttributeError : No title for this product")
        """try: 
            products_with_AttributeError_for_product_description_extraction.append(title_extraction(soup_product, "")) 
            print("AttributeError : No title for this product")
        except AttributeError:
            #No list required as this function is not used here to register the title
            pass"""
    products_descriptions_list.append(product_description)
    return product_description


def category_extraction(soup_product, categories_list):
    """Returns category from soup_product"""

    breadcrumb_class = soup_product.find(class_="breadcrumb")
    breadcrumb_class_lis = breadcrumb_class.findAll("li")
    breadcrumb_class_lis_a = breadcrumb_class_lis[2]
    category = breadcrumb_class_lis_a.find("a").string
    categories_list.append(category)

    return category 


def review_rating_extraction(soup_product, review_ratings_list):
    """Returns review_rating from soup_product"""

    #NB: i tried with """ print(paragraph["class_"]) """" : key error
    paragraphs_attributes = []
    paragraphs = soup_product.findAll("p")
    for paragraph in paragraphs:
        paragraphs_attributes.append(paragraph.attrs)
    for paragraphs_attribute in paragraphs_attributes:
        for key in paragraphs_attribute:
            if key == "class":
                if paragraphs_attribute[key][0] == "star-rating":
                    review_rating_string = paragraphs_attribute[key][1]
    review_rating = review_rating_string_int_correspondance[review_rating_string]
    review_ratings_list.append(review_rating)

    return review_rating


def image_url_extraction(soup_product, images_urls_list):
    """Returns image_url from soup_product"""

    item_active = soup_product.find(class_ ="item active")
    image = item_active.find("img") 
    image_url = "http://books.toscrape.com" + image["src"][5:]
    images_urls_list.append(image_url)
    
    return image_url


def soup_product_information_extraction(requests_web_page_product, soup_product, product_information, product_page_urls_list, universal_product_codes_list, titles_list, prices_including_tax_list, prices_excluding_tax_list, numbers_available_list, products_descriptions_list, categories_list, review_ratings_list, images_urls_list):
    """Extraction of information asked by the step 1 of the OpenClassRoom project"""

    #URL
    product_page_url = product_page_urls_list_extraction(requests_web_page_product, product_page_urls_list)

    #UPC
    universal_product_code = universal_product_code_extraction(product_information, universal_product_codes_list)

    #Title
    title = title_extraction(soup_product, titles_list)

    #Price including tax
    price_including_tax = price_including_tax_extraction(product_information, prices_including_tax_list)

    #Price excluding tax
    price_excluding_tax = price_excluding_tax_extraction(product_information, prices_excluding_tax_list)

    #Availability
    number_available = number_available_extraction(product_information, numbers_available_list)

    #Product description
    product_description = product_description_extraction(soup_product, products_descriptions_list)

    #Category
    category = category_extraction(soup_product, categories_list)

    #Review rating
    review_rating = review_rating_extraction(soup_product, review_ratings_list)

    #Image URL
    image_url = image_url_extraction(soup_product, images_urls_list)

    #TEST
    #print("product_page_url", product_page_url)
    #print("")
    #print("universal_product_code", universal_product_code)
    #print("")
    #print("title", title)
    #print("")
    #print("price_including_tax", price_including_tax)
    #print("")
    #print("price_excluding_tax", price_excluding_tax)
    #print("")
    #print("number_available", number_available)
    #print("")
    #print("product_description", product_description)
    #print("")
    #print("category", category)
    #print("")
    #print("review_rating", review_rating)
    #print("")
    #print("image_url", image_url)
    print("Extraction of product information done for : {0}".format(title))


products_with_UnicodeEncodeError_for_information_loading_csv = []


def product_information_loading_csv_format(url_category, product_page_urls_list, universal_product_codes_list, titles_list, prices_including_tax_list, prices_excluding_tax_list, numbers_available_list, products_descriptions_list, categories_list, review_ratings_list, images_urls_list):
    """Writes product information in a CSV file"""

    global products_with_UnicodeEncodeError_for_information_loading_csv

    #Definition of the table headers
    table_headers = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]

    #New CSV file creation
    url_category_prefix = url_category[-3:-1]
    url_category_name = url_category[51:-3]

    print("url_category_name" + url_category_name)

    with open('scraping_CSV_files/{0}_books_toscrap_category_{1}.csv'.format(url_category_prefix.replace("_", "0"), url_category_name), 'w') as csv_file:
    
    #Creation of a 'writer' object
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(table_headers)

        #Definition of a line : information from python lists/tables [] from soup_product_information_extraction

        for product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url in zip(product_page_urls_list, universal_product_codes_list, titles_list, prices_including_tax_list, prices_excluding_tax_list, numbers_available_list, products_descriptions_list, categories_list, review_ratings_list, images_urls_list) :
            line = [product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url]

            #Writing each line in the CSV file 
            try:
                csv_writer.writerow(line)
                #print("CSV writing of product information done for : {0}".format(title))       -->      TOO MUCH PRINTS; DO NOT UNDERSTAND
                #print("CSV writing of product information done for : {0}".format(line[2]))
            except UnicodeEncodeError:
                #raise Exception("UnicodeEncodeError found")
                #products_with_UnicodeEncodeError_for_information_loading_csv.append(line[2])
                products_with_UnicodeEncodeError_for_information_loading_csv.append(title)
                print("UnicodeEncodeError found")



complete_product_urls_list_reinitizaliation = True

def listing_products_urls_from_category(url_category, url_category_pageX =""):
    """Extracts and returns URLs of all products of a CATEGORY"""
    """url_category_pageX is empty; then , it takes "page2", "page3", etc as value, to complete the url"""

    #Reinitialization of the list of urls of products, if the category changes ; if we are on a "next" page, we keep the list a complete it
    global complete_product_urls_list_reinitizaliation
    global complete_product_urls_list

    if complete_product_urls_list_reinitizaliation == True:
        complete_product_urls_list = []
    else:
        complete_product_urls_list = complete_product_urls_list

    #Creation of a requests and a soup objects corresponding to a category page
    requests_web_page_category = requests.get(url_category + url_category_pageX)
    soup_category = BeautifulSoup(requests_web_page_category.content, "html.parser")

    #Extraction of links of each products of a category, from the URL of the category
        #category_ol_class_row : searching the element "ol" with class "row"
    category_ol_class_row = soup_category.find("ol", class_ = "row")

        #category_ol_li_class_col_xs : searching the element "li" with class "col_xs..." WITHIN the element ol previously found
    category_ol_li_class_col_xs = category_ol_class_row.findAll(class_ = "col-xs-6 col-sm-4 col-md-3 col-lg-3")

    for lis in category_ol_li_class_col_xs:
        #print(lis)
        category_ol_li_article = lis.find("article")
        category_ol_li_article_div = category_ol_li_article.find("div", class_ = "image_container")
        category_ol_li_article_div_a = category_ol_li_article_div.find("a")
        category_ol_li_article_div_a_href = category_ol_li_article_div_a["href"] 
        complete_product_link = "http://books.toscrape.com/catalogue" + category_ol_li_article_div_a_href[8:]
        
        complete_product_urls_list.append(complete_product_link)

    #RECURSIVITY 
    category_li_class_next = soup_category.find("li", class_ = "next")

    if category_li_class_next == None:
        print("No NEXT button")
        complete_product_urls_list_reinitizaliation = True
        pass
    
    elif category_li_class_next != None:
        complete_product_urls_list_reinitizaliation = False
        
        #Identification of the link for the next page
        category_li_link_a = category_li_class_next.find("a")
        url_category_pageX = category_li_link_a["href"]
        ##category_li_link_a_href = category_li_link_a["href"] 
        ##next_page_link = url_category + category_li_link_a_href
        print("There is a NEXT button towards the adress {0}".format(url_category + url_category_pageX))
        listing_products_urls_from_category(url_category, url_category_pageX) #RECURSIVITY.

    else: 
        print("error")
        pass

    print("All products url has been listed for the category {0}".format(url_category + url_category_pageX))
    return complete_product_urls_list




url_complete_book_category_without_indexHtml_list = []

def listing_category_urls_from_website(url_book_to_scrap):
    """Extracts and returns URLs of all categories of a website"""

    #Creation of a requests and a soup objects corresponding to a website index.html page
    requests_web_page_book_to_scrap = requests.get(url_book_to_scrap)
    soup_book_to_scrap = BeautifulSoup(requests_web_page_book_to_scrap.content, "html.parser")

    #Extraction of links of each category of the website, from the URL of the index.html page of the website 
    book_to_scrap_div_side_books_categories = soup_book_to_scrap.find(class_ = "side_categories")
    book_to_scrap_ul_navigation_list_books_categories = book_to_scrap_div_side_books_categories.find(class_ = "nav nav-list") 
    book_to_scrap_books_categories_list = book_to_scrap_ul_navigation_list_books_categories.findAll("li")[1:] #[1:] --> exclusion of "Books": not a category
    for lis in book_to_scrap_books_categories_list:
        link_a_book_categorie = lis.find("a")
        
        link_a_href_book_categorie = link_a_book_categorie["href"]
        url_complete_book_category = "http://books.toscrape.com/" + link_a_href_book_categorie
        url_complete_book_category_without_indexHtml = url_complete_book_category[:-10]

        name_book_category = link_a_book_categorie.string[62:-54] #spaces before the name

        print("URL for '{0}' category found at : {1}".format(name_book_category, url_complete_book_category))
        
        url_complete_book_category_without_indexHtml_list.append(url_complete_book_category_without_indexHtml)

    return url_complete_book_category_without_indexHtml_list


def scraping_CSV_files_folder_initialization():
    mkdir("scraping_CSV_files")
    print("The folder 'scraping_CSV_files' has been created and will contain the CSV files resulting from the ETL process")


def scraping_products_pictures_folder_initialization():
    mkdir("scraping_products_pictures")
    print("The folder 'scraping_products_pictures' has been created and will contain the pictures downladed from the ETL process")


def product_picture_downloading(url_book_to_scrap, soup_product):

    picture_url_src = soup_product.find("div", id = "product_gallery").find("div", class_="thumbnail").find("div", class_="carousel-inner").find("div", class_="item active").find("img")["src"]
    complete_picture_url = url_book_to_scrap[:-10] + picture_url_src[6:]
    print(complete_picture_url)

    picture_file_name = soup_product.find(class_ = "active").string # = the name, but i do not use the function  title_extraction as it requires a table)
    picture_file_name_withPath_withoutSlash_withoutTwoPoints_withoutInterogationPoint_withoutAsterix_withoutComma_limitedTo20Car_jpg = "scraping_products_pictures/" + picture_file_name[:20].replace("/", "_").replace(":", "__").replace("?", "___").replace("*", "____").replace('"', "___") +  ".jpg"
    picture_file = open(picture_file_name_withPath_withoutSlash_withoutTwoPoints_withoutInterogationPoint_withoutAsterix_withoutComma_limitedTo20Car_jpg, "wb") #did not work if I kept all the picture_file_name: too long I guess, so I decided to take the 20 first letters

    requests_picture_product = requests.get(complete_picture_url)

    picture_file.write(requests_picture_product.content)
    picture_file.close

    print("Picture download successful")
    


def main(url_book_to_scrap):
    """ . """      

    scraping_CSV_files_folder_initialization()
    scraping_products_pictures_folder_initialization()

    print("")
    print("== CATEGORIES FOUND ON THE WEBSITE {0} ==".format(url_book_to_scrap))
    print("")
    url_complete_book_category_without_indexHtml_list = listing_category_urls_from_website(url_book_to_scrap)
    for url_category in url_complete_book_category_without_indexHtml_list: 

        #Reinitialization of the tables for each category
        product_page_urls_list = tables_for_product_information_extraction_initialization()[0]
        universal_product_codes_list = tables_for_product_information_extraction_initialization()[1]
        titles_list = tables_for_product_information_extraction_initialization()[2]
        prices_including_tax_list = tables_for_product_information_extraction_initialization()[3]
        prices_excluding_tax_list = tables_for_product_information_extraction_initialization()[4]
        numbers_available_list = tables_for_product_information_extraction_initialization()[5]
        products_descriptions_list = tables_for_product_information_extraction_initialization()[6]
        categories_list = tables_for_product_information_extraction_initialization()[7]
        review_ratings_list = tables_for_product_information_extraction_initialization()[8]
        images_urls_list = tables_for_product_information_extraction_initialization()[9]
        #racourcir avec a,b,c = x,y,z ?

        print("")
        print("==== PRODUCTS FOUND FOR EACH CATEGORY ====")
        print("")
        """ Extraction of products urls from one category url """
        complete_product_urls_list = listing_products_urls_from_category(url_category)
        for complete_product_url in complete_product_urls_list: 

            """ ETL at product scale"""
            """
            Requests and Soup objects initialization; 
            Information, (from table) extraction
            Extraction of all information asked; and save in python tables []
            """
            print("====== PRODUCT ETL ======")
            print(complete_product_url)
            requests_web_page_product = requests_web_page_product_initialization(complete_product_url)
            soup_product = soup_product_initialization(requests_web_page_product)
            soup_product_information_table = soup_product_information_table_initialization(soup_product)
            
            soup_product_information_extraction(requests_web_page_product, soup_product, soup_product_information_table, product_page_urls_list, universal_product_codes_list, titles_list, prices_including_tax_list, prices_excluding_tax_list, numbers_available_list, products_descriptions_list, categories_list, review_ratings_list, images_urls_list)


            """Picture downloading"""
            product_picture_downloading(url_book_to_scrap, soup_product)

        """ Writing in CSV file """
        product_information_loading_csv_format(url_category, product_page_urls_list, universal_product_codes_list, titles_list, prices_including_tax_list, prices_excluding_tax_list, numbers_available_list, products_descriptions_list, categories_list, review_ratings_list, images_urls_list)
        print("")

    print("")
    print("")
    print("================================ CONCLUSION ================================")
    print("")
    print("UnicodeEncodeError was/were found during CSV loading for the following products {0}".format(products_with_UnicodeEncodeError_for_information_loading_csv))
    print("")
    print("The product_description was not found for the following products: {0}".format(products_with_AttributeError_for_product_description_extraction))
    print("")
    print("ETL performed for each product of the {0} website: performed with success. Errors which happenned during the execution are listed hereunder".format(url_book_to_scrap))
    print("")

main("http://books.toscrape.com/index.html")
