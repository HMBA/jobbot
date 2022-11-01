import sys
import time
from utils import Utils

class Main:

    def __init__(self) -> None:
        try:
            # Getting arguments
            self.args = self.get_args()  
            self.region = self.args[0]          
            self.job_search = self.args[1]
            self.expiry_date = self.args[2] 

            self.utils = Utils()
            self.search_jobs()
        
        except IndexError:
            print("Must Pass 3 Params. Job Search and Expiry Date!\nExample:\npython3 main.py 'ng' 'Web Developer' '10/20/2022'")

    def get_args(self):
        n = len(sys.argv)
        args = []

        for i in range(1, n):
            args.append(sys.argv[i])
        
        return args

    def search_jobs(self):
        # Getting start time
        start_time = time.time()

        # Getting jobs
        print('Getting Jobs...')
        jobs = self.utils.search_jobs(self.region, self.job_search)
        print('Operation Successful!\nJobs Scrapped:', len(jobs))

        # Getting end time
        end_time = time.time()

        # Calculating program runtime
        print("Script execution time: %s seconds" % round(end_time - start_time))

main = Main()