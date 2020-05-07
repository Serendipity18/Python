'''
Created on Nov 7, 2019
    Web Scrapes my_url from NewEgg to parse out
    the Brand, Product Name, Cost, Shipping, and then 
    mathematically calculates the Total Price. After parsing
    the information it is written to the outWorkbook excel file.
@author: Josh
'''
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import xlsxwriter

outWorkbook = xlsxwriter.Workbook("Graphics Cards.xlsx")
outSheet = outWorkbook.add_worksheet()
bold = outWorkbook.add_format({'bold': True})

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


def WebScraperHeaders(outSheet):
    headers = ["Brand", "Product_Name", "Cost", "Shipping", "Total_price"]
    # position counters
    yCounter = 0
    xCounter = 0
    # for loop to write the headers along the X axis
    for x in headers:
        outSheet.write(yCounter, xCounter, x, bold)
        xCounter += 1
    yCounter += 1
    WebScraperContent(outSheet, yCounter)


def WebScraperContent(outSheet, yCounter):    
    brand_list = []
    product_list = []
    shipping_list = []
    cell_length1 = 0
    cell_length2 = 0
    cell_length3 = 0
    # for loop to grab all the products parsed information
    for container in containers:
        # brand of the product
        brand_container = container.findAll("a", "item-brand")
        brand = brand_container[0].img["title"]
        brand_list.append(brand)

        # name of the product
        title_container = container.findAll("a", {"class":"item-title"})
        product_name = title_container[0].text.replace(",", " | ")
        product_list.append(product_name)

        # shipping price of the product
        shipping_container = container.findAll("li", {"class":"price-ship"})
        shipping = shipping_container[0].text.strip().replace(" Shipping", "")
        
        # strips the "$" sign from the stripping string
        if shipping.startswith("$"):
            shipping = shipping.replace("$", "")
        else:
            pass
            
        # if the shipping is equal to the string "Free" change it to 0 to be added to total cost
        if shipping == "Free":
            shipping = "0.00"
        else:
            pass
        
        shipping_list.append(shipping)
                   
        list_container = container.findAll("li", {"class": "price-current"})
        list_cost = list_container[0].strong.get_text().replace(",", "") + list_container[0].sup.get_text()
        
        list_cost = float(list_cost)
        shipping = float(shipping)
        
        total_price = round((list_cost * float(1.13) + shipping), 2)

        # prints the parsed information from each each graphics card to an excel file
        content_list = [brand, product_name, list_cost, shipping, total_price]
        xCounter = 0
        for i in content_list:
            brand_list.sort()
            outSheet.write(yCounter, xCounter, i)
            xCounter += 1
        yCounter += 1
    
    # finds the longest length of each variable to format the excel sheet
    for i in brand_list:
            if len(i) > cell_length1:
                cell_length1 = len(i)
    for i in product_list:
            if len(i) > cell_length2:
                cell_length2 = len(i)
    for i in shipping_list:
            if len(i) > cell_length3:
                cell_length3 = len(i)   
    outSheet.set_column('A:A', cell_length1)
    outSheet.set_column('B:B', cell_length2)
    outSheet.set_column('D:D', cell_length3)


WebScraperHeaders(outSheet)
outWorkbook.close()
