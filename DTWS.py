import math, requests, csv, os, smtplib, ssl
from bs4 import BeautifulSoup

# URL includes the filter 'May live with... Dogs'
DT_base_url = "https://www.dogstrust.org.uk/rehoming/dogs/filters/~~~~~n~~d/page/"
# pylint: disable=anomalous-backslash-in-string
old_CSV_data_path = "data\previous-dogs.csv"
new_CSV_data_path = "data\current-dogs.csv"
updates_csv_path = r"data\updates.csv"
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
    
    def __iter__(self):
        return iter([self.name, self.breed, self.location])

def parse_and_save(index):
    dog_name = soup.select(dog_info_link + str(index) + "> h3")[0].text.strip()
    dog_breed = soup.select(dog_info_link + str(index) + "> span")[0].text.strip()
    dog_location = soup.select(dog_info_link + str(index) + "> span > strong")[0].text.strip()

    # Populate new Dog object and add to all_dogs list
    current_dog = Dog(dog_name, dog_breed, dog_location)
    all_dogs.append(current_dog)

    print("Saving... " + current_dog.name)

def make_csv(allDogs):

    # Check for and if needed delete old "current" file
    if os.path.exists("data\current-dogs.csv"):
        os.remove("data\current-dogs.csv")

    # Open CSV in Write mode
    with open(new_CSV_data_path, 'w+') as dog_data:
        wr = csv.writer(dog_data, delimiter=",")
        for dog in allDogs:
            wr.writerow([dog.name, dog.breed, dog.location])

def compare_csv(old_csv_path, new_csv_path, update_csv_path):
    
    dogs_added: bool = False
    dogs_removed: bool = False

    # Open both CSVs in read mode
    with open(old_csv_path, 'r') as old_csv, open(new_csv_path, 'r') as new_csv:
        old_data = old_csv.readlines()
        new_data = new_csv.readlines()

    with open(update_csv_path, 'w') as outputFile:
        # Checking for dogs added to site
        for line in new_data:
            if line not in old_data:
                outputFile.write("ADDED: " + line)
                dogs_added = True
        # Checking for dogs removed from site
        for line in old_data:
            if line not in new_data:
                outputFile.write("REMOVED: " + line)
                dogs_removed = True
    
    # A better way to do this could be with a response string var that is added to based on conditionals and then printed at the end
    if dogs_added == True:
        if dogs_removed == True:
            print("\nNew dogs added and some rehomed!\n Results saved to: " + updates_csv_path)
        else:
            print("\nNew dogs added!\nResults saved to: " + updates_csv_path)
        
        # Send email notification

    elif dogs_removed == True:
        print("\nSome dogs were rehomed!\nResults saved to: " + updates_csv_path)
    else:
        print("\nNo updates! Please check again later.")

def replace_csv():
    base_path = r"D:\Python\Dogs Trust Web Scraper\data"
    # Check for and remove old data
    if os.path.exists(r"data\previous-dogs.csv"):
        os.remove(r"data\previous-dogs.csv")
        # Rename current data as previous for the next run
        os.rename(os.path.join(base_path, "current-dogs.csv"), os.path.join(base_path, "previous-dogs.csv"))

def send_email(to_address):
    # SSL port
    port = 465
    username = os.environ.get("DTWSEmail")
    password = os.environ.get("DTWSPassword")

    # Create secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(username, password)

'''
    Main Function starts here
'''

print("Attempting connection to Dogs Trust site...\n")

if (req_status == 200):

    print("Successfully connected to site...")

    print("Starting Scan...\n")

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

    print("\nCompiling data into CSV...")
    make_csv(all_dogs)

    print("Checking for updates...")
    compare_csv(old_CSV_data_path, new_CSV_data_path, updates_csv_path)

    print("\nStored data updating...")
    replace_csv()

    print("\n\t - Scan Complete! -")

else:
    print("Connection to site failed.\nPlease check you are connected to the internet by visiting:\n\nhttps://www.dogstrust.org.uk")
