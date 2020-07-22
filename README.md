# Dogs Trust Web Scraper

## How it Works

The DTWS script web scrapes the Dogs Trust site looking for Dogs who can live with other dogs.  
*(This may be improved in future to allow custom filters to be applied)*

It parses the data - Name, Breed, Location, Profile URL - and saves it into a CSV.

It then compares the compiled data with the data from a previous run, saving any changes.  
If it detects changes you can configure it to send you an email notification which will be covered in more detail below.

## Setup - Email Notifications
### Create an Account
The first step is to setup a new gmail account. This is just to keep it separate from your normal account and adds a buffer in the event that the credentials for the account are exposed.
### Leveraging Environment Variables
To avoid exposing credentials in the code you can setup environment variables on your local machine to hold your email address and password.  
A detailed explanation of how to do this can be found [here](https://saralgyaan.com/posts/set-passwords-and-secret-keys-in-environment-variables-maclinuxwindows-python-quicktip/).

```
    sender_email = os.environ.get("DTWSEmail")
    receiver_email = os.environ.get("MyEmail")
    password = os.environ.get("MyPassword")
```

All you'll need to do is change the arguments e.g. `MyEmail` to whatever you named your env. variables.

## Setup - Automating Scans
The aim of this script is to make it easier for you to know when new dogs are added so you can put your application in as soon as possible.  
Having to frequently run the script manually and remembering to do it defeats the purpose so the following is a solution that will make it much easier.  

### Create a Batch Script
The batch script is a simple way to execute the script and it should take the form:  
For Automation:
```
cd <Folder with your script in it>
"<Path to your python.exe>" "Path to your script" %*
```
Here's an example of what it may look like, bear in mind that you can skip the `cd` if you place the batch script in the same directory as your python script:
```
cd /D "D:\Python\Dogs Trust Web Scraper"
"C:\Program Files (x86)\Python38-32\python.exe" "DTWS.py" %*
```
If you plan to run it manually add a `pause` at the end on it's own line to stop the terminal closing immediately on.

### Create a Task in Task Scheduler (Windows)
Finally, you'll need to create a Task that will run the batch script on a time interval - I have mine run every hour between 9am and 5pm. In Windows you can use the Task Scheduler to achieve this.  
This is fairly easy to do but if you are ensure there is a useful guide [here](https://datatofish.com/python-script-windows-scheduler/).

---

### Please visit Dogs Trust to see if you can give a dog a home!
https://www.dogstrust.org.uk