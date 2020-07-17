import math, requests
from bs4 import BeautifulSoup

# URL includes the filter 'May live with... Dogs'
DT_base_url = "https://www.dogstrust.org.uk/rehoming/dogs/filters/~~~~~n~~d/page/"
# Create initial page object to find total dogs - vars will be overwritten in loop
current_page = requests.get(DT_base_url + "1")
req_status = current_page.status_code
soup = BeautifulSoup(current_page.content, 'html.parser')
total_dogs = int(soup.find('strong').get_text())
# Required to re-declare as int again due to math.ceil returning a float
num_pages = int(math.ceil((total_dogs) / 12))
dog_info_link = "#BodyContent_DogList1_rptDogList_lnkDog_"
# Initialise list to hold all dogs' info
all_dogs = []

####################

class Dog:
    def __init__(self, name, breed, location):
        self.name = name
        self.breed = breed
        self.location = location

def parse_and_save(index):
    dog_name = soup.select(dog_info_link + str(index) + "> h3")[0].text.strip()
    dog_breed = soup.select(dog_info_link + str(index) + "> span")[0].text.strip()
    dog_location = soup.select(dog_info_link + str(index) + "> span > strong")[0].text.strip()

    # Populate new Dog object and add to all_dogs list
    current_dog = Dog(dog_name, dog_breed, dog_location)
    all_dogs.append(current_dog)

    print("Saving... " + current_dog.name)

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
        parse_and_save(j)

# Handle elements on last page
last_page = requests.get(DT_base_url + str(num_pages))
soup = BeautifulSoup(last_page.content, 'html.parser')
dogs_on_last_page = total_dogs % 12
print("\nPAGE: " + str(num_pages))
for i in range(0, dogs_on_last_page):
    parse_and_save(i)
