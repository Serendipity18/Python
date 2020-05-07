'''
Created on Nov 5, 2019
This is my first attempt at making a webscraper with beautifulsoup, but later created a version 2 that works much better.
@author: Josh
'''
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.newegg.ca/p/pl?N=100007708%20600419577%20600536666%20601194948%20601202919%20601203901%20601203927%20601205646\
%20601294835%20601295933%20601296377%20601296379%20601301599%20601305993%20601321572%20601323902%20601326374%20601328427%20601331379%\
20601341679%204814&cm_sp=Cat_video-Cards_1-_-Visnav-_-Gaming-Video-Cards_2'

# opening up connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# grabs each product
containers = page_soup.findAll("div", {"class":"item-container"})
container = containers[0]


def WebScraper(container):
    # opens the csv file for writing
    with open("Products.csv", "w") as file:
        headers = "Brand, Product_name, Cost, Shipping, Total_price\n"
        file.write(headers)
        # for loop to grab all products and write them to the file
        for container in containers:
            # brand of the product
            brand_container = container.findAll("a", "item-brand")
            brand = brand_container[0].img["title"]

            # name of the product
            title_container = container.findAll("a", {"class":"item-title"})
            product_name = title_container[0].text

            # shipping price of the product
            shipping_container = container.findAll("li", {"class":"price-ship"})
            shipping = shipping_container[0].text.strip().replace("Shipping", "")
            
            # if the shipping is equal to the string "Free " change it to 0 to be added later on
            if shipping == "Free ":
                shipping = "$0.00"
            else:
                pass
            
            list_cost = container.findAll("li", {"class": "price-current"})
            list_cost1 = list_cost[0].strong.get_text() + list_cost[0].sup.get_text()
            # not the total price, needs shipping
            total_price = float(list_cost1.replace(",", "")) * float(1.13) + float(shipping.replace("$", ""))
            
            # writes to the file and replaces "," with " | "
            file.write(brand \
                       +"," \
                       +product_name.replace(",", " | ") \
                       +"," \
                       +"$" \
                       +list_cost1.replace(",", "") \
                       +"," \
                       +shipping \
                       +"," \
                       +"$" \
                       +str(round(total_price, 2)).replace(",", "") \
                       +"\n")


WebScraper(container)
