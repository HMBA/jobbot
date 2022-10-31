import sys
from utils import Utils

class Main:

    def __init__(self) -> None:
        try:
            self.args = self.get_args()            
            self.job_search = self.args[0]
            self.expiry_date = self.args[1] 
            self.utils = Utils()
            self.search_jobs()
        
        except IndexError:
            print("Must Pass 2 Params. Job Search and Expiry Date!\nExample:\npython3 main.py 'Web Developer' '10/20/2022'")

    def get_args(self):
        n = len(sys.argv)
        args = []

        for i in range(1, n):
            args.append(sys.argv[i])
        
        return args

    def search_jobs(self):
        self.utils.search_jobs(self.job_search)


main = Main()