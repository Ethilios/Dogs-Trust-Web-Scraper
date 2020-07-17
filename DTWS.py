import math, requests
from bs4 import BeautifulSoup

DT_base_url = "https://www.dogstrust.org.uk/rehoming/dogs/filters/~~~~~n~~d/page/"
# Use array of objects here would be better
dog_list = []
# Create initial page object to find total dogs - vars will be overwritten in loop
current_page = requests.get(DT_base_url + "1")
req_status = current_page.status_code
soup = BeautifulSoup(current_page.content, 'html.parser')
total_dogs = int(soup.find('strong').get_text())
# Required to declare as int again due to math.ceil returning a float
num_pages = int(math.ceil((total_dogs) / 12))

print("Starting Scan...\n")

if (req_status == 200):
    print("Successfully connected to site...") 
else:
    print("Connection to site failed.")
     
print("Total dogs on site: " + str(total_dogs))
print("Pages: " + str(num_pages))

# Loop through pages - except last page - see below
for i in range(1,num_pages):
    print("\nPAGE: " + str(i))
    current_page = requests.get(DT_base_url + str(i))
    soup = BeautifulSoup(current_page.content, 'html.parser')
    # Loop through elements on each page
    for j in range(0,12):
        current_el = soup.select("#BodyContent_DogList1_rptDogList_lnkDog_" + str(j) + "> h3")
        dog_list += current_el[0].text.strip()
        print("\t - " + current_el[0].text.strip())

# Handle elements on last page
last_page = requests.get(DT_base_url + str(num_pages))
soup = BeautifulSoup(last_page.content, 'html.parser')
dogs_on_last_page = total_dogs % 12
print("\nPAGE: " + str(num_pages))
for i in range(0, dogs_on_last_page):
    current_el = soup.select("#BodyContent_DogList1_rptDogList_lnkDog_" + str(i) + "> h3")
    dog_list += current_el[0].text.strip()
    print("\t - " + current_el[0].text.strip())
