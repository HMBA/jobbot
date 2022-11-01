from time import sleep
from selenium import webdriver

class Utils:

    def __init__(self) -> None:
        # Set driver executable path
        self.driver = webdriver.Chrome(executable_path='/Users/apple/Desktop/GoWork Web Scrapping (Python)/chromedriver')

        # Setting Xpath for elements of indeed web page
        self.x_paths = {}
        self.x_paths['li_list'] = '/html/body/main/div/div[1]/div/div/div[5]/div[1]/div[5]/div/ul/li'
        self.x_paths['next_arrow_button_page1'] = '/html/body/main/div/div[1]/div/div/div[5]/div[1]/nav/div[6]/a'
        self.x_paths['next_arrow_button_page2'] = '/html/body/main/div/div[1]/div/div/div[5]/div[1]/nav/div[7]/a'

    
    """
    Looping through each page and adding job to the jobs per list
    and then adding jobs per page to the jobs_per_page list
    and then returning jobs_per_page list
    """
    def get_data(self, url: str):
        # HEADERS ={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
        self.driver.get(url)
        jobs_per_page = []
        jobs = []
        count = 0
        try:
            while(True):
                sleep(2)

                # Getting jobs
                li_list = self.driver.find_elements('xpath', self.x_paths['li_list'])
                
                # Adding jobs in our jobs list
                for i in range(len(li_list)):
                    li = li_list[i]
                    job = li.text.split("\n")
                    jobs.append(job)

                # Adding jobs list in jobs_per_page list
                jobs_per_page.append(jobs)
                next_arrow_button = None
                print("Page:", len(jobs_per_page))

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
            return jobs_per_page

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
        print(url)
            
        """
        Scrapping on the created URL above and 
        returning the jobs 
        """
        job_data = self.get_data(url)

        # Printing the returned jobs
        for jobs in job_data:
            print("\n\n========================\n\n")
            for job in jobs:
                print(job, end="\n===============\n")
        


