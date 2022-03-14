from bs4 import BeautifulSoup
import requests
import pandas as pd 

def extract_page(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'}
    url = f'https://uk.indeed.com/jobs?q=python&l=London&start={page}'
    result = requests.get(url, headers)
    html_file = BeautifulSoup(result.text, "html.parser")
    return html_file


def retrieve_file(html_file):
    job_card = html_file.find_all('div', class_='job_seen_beacon')
    for job in job_card:
        title = job.find('h2').text.strip()
        company = job.find('span', class_ ="companyName").text
        try:
            salary = job.find('div', class_='metadata salary-snippet-container').text
        except:
            salary = 'None'
        
        job_dict = {
            'title': title,
            'company': company,
            'salary': salary
        }
        job_list.append(job_dict)
    return job_list


job_list = []
for i in range(0,60,10):
    page_list = extract_page(i)
    retrieve_file(page_list)  

df = pd.DataFrame(job_list)
df.to_csv('python_jobs_list.csv')
   

