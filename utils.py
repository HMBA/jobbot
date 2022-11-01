from time import sleep
from selenium import webdriver

class Utils:

    def __init__(self) -> None:
        # Configurations
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'   
        executable_path = './chromedriver'

        # Setting driver options
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        op.add_argument("--window-size=1920x1080") 
        op.add_argument('user-agent={0}'.format(user_agent))

        # Creating driver
        self.driver = webdriver.Chrome(executable_path= executable_path, options=op)

        # Setting Xpath for elements of indeed web page
        self.x_paths = {}
        self.x_paths['next_arrow_button_page1'] = '/html/body/main/div/div[1]/div/div/div[5]/div[1]/nav/div[6]/a'
        self.x_paths['next_arrow_button_page2'] = '/html/body/main/div/div[1]/div/div/div[5]/div[1]/nav/div[7]/a'

    
    """
    Looping through each page and adding job to the jobs list
    """
    def get_data(self, url: str):
        # HEADERS ={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
        self.driver.get(url)
        jobs = []
        count = 0
        try:
            while(True):
                sleep(2)

                # Getting jobs
                table1 = self.driver.find_elements('class name', 'jobCard_mainContent')
                table2 = self.driver.find_elements('class name', 'jobCardShelfContainer')

                # Add job object to jobs list
                for i in range(len(table1)):
                    table1_text_split = table1[i].text.split("\n")
                    table2_text_split = table2[i].text.split("\n")

                    # Creating job object
                    job_title = table1_text_split[0]
                    job_company = table1_text_split[2] if table1_text_split[1] == 'new' else table1_text_split[1]
                    job_location = table1_text_split[3] if table1_text_split[1] == 'new' else table1_text_split[2]
                    job_type = table1_text_split[len(table1_text_split) - 1]

                    job_description = ""

                    for a in range(len(table2_text_split)):
                        if a != len(table2_text_split) - 2:
                            job_description += table2_text_split[a]
                        else:
                            break
                    job = Job(job_title, job_company, job_location, job_type, job_description)
                    # Adding object to jobs list
                    jobs.append(job)

                
                next_arrow_button = None

                # If on first page 
                if count == 0:
                    next_arrow_button = self.driver.find_element('xpath', self.x_paths['next_arrow_button_page1'])
                    count += 1
                # If page is greater than 1
                else:
                    try:
                        # Try this xpath if it doesn't work try the other one
                        next_arrow_button = self.driver.find_element('xpath', self.x_paths['next_arrow_button_page2'])
                    except Exception:
                        try:
                            # If this xpath also doesn't work we stop the while loop
                            next_arrow_button = self.driver.find_element('xpath', self.x_paths['next_arrow_button_page1'])
                        except Exception:
                            # Get out of while loop if next_arrow button is not found
                            break
                
                # click the next_arrow_button
                next_arrow_button.click()

        except Exception as e:
            print(e.args)
        finally:
            # Close the browser
            self.driver.quit()

            # return jobs
            return jobs

    """
    Main Function to control the searching of jobs
    on the provided region and job keywords
    """
    def search_jobs(self, region: str, job_name: str):

        """
        Arranging data for the job search
        Creating the url request for the job scrapping
        """
        job_name_split = job_name.split(" ")
        base_url = "https://" + region + ".indeed.com/"

        url = base_url

        url = base_url + "jobs?q="
        for i in range(len(job_name_split)):
            name = job_name_split[i]

            if i == len(job_name_split) - 1:
                url += name
            else:
                url += name + "+"
            
        """
        Scrapping on the created URL above and 
        returning the jobs 
        """
        jobs_data = self.get_data(url)

        # Returning jobs data
        return jobs_data
        


class Job:

    def __init__(self, title: str, company: str, location: str, job_type: str, job_description: str) -> None:
        self.title = title
        self.company = company
        self.location = location
        self.job_type = job_type
        self.job_description = job_description

    def get_title(self):
        return self.title

    def get_company(self):
        return self.company

    def get_location(self):
        return self.location

    def get_job_type(self):
        return self.job_type

    def get_job_description(self):
        return self.job_description

    def __str__(self) -> str:
        returnString = f"Title: {self.title}\nCompany: {self.company}\nLocation: {self.location}\nJob Type: {self.job_type}\nJob Description: {self.job_description}"
        return returnString