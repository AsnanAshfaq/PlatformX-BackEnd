from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import uuid

artificial_urls_list = [
    "https://www.brookings.edu/research/how-artificial-intelligence-is-transforming-the-world/",
    "https://futureoflife.org/background/benefits-risks-of-artificial-intelligence/?cn-reloaded=1"
]

cyber_urls_list = [
    "https://www.kaspersky.com/resource-center/definitions/what-is-cyber-security",
    "https://www.upguard.com/blog/cybersecurity-important"
]

data_science_urls_list = [
    "https://searchenterpriseai.techtarget.com/definition/data-science",
]

block_chain_urls_list = [
    "https://builtin.com/blockchain"
]

vr_urls_list = [
    "https://www.sciencedaily.com/terms/virtual_reality.htm"
]

dev_ops_urls_list = [
    "https://www.toptal.com/insights/innovation/what-is-devops"
]

url = "https://www.brookings.edu/research/how-artificial-intelligence-is-transforming-the-world/"


# "https://builtin.com/artificial-intelligence",
#     "https://futureoflife.org/background/benefits-risks-of-artificial-intelligence/?cn-reloaded=1",
#     "https://www.brookings.edu/research/how-artificial-intelligence-is-transforming-the-world/",
#     "https://wsimag.com/science-and-technology/64215-artificial-intelligence-has-changed-our-world"

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def scrape_articles(request):
    response = []
    driver = webdriver.Chrome(executable_path="C:/chromedriver.exe")
    try:
        for index, link in enumerate(artificial_urls_list):
            if index == 0:
                driver.get(link)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                title = soup.find(name="h1", class_="report-title").string
                content = soup.find(name="div", class_="summary-text").p.string
                image = soup.source['srcset']
                data = {
                    "id": uuid.uuid4(),
                    "title": title,
                    "content": content,
                    "image": image,
                    "url": link
                }
                response.append(data)

        for index, link in enumerate(cyber_urls_list):
            if index == 0:
                driver.get(link)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                title = soup.find(name="h1", class_="PageHeadline_title__f5SGz").string
                content = soup.find(name="p", class_="MsoNormal").string
                image = soup.find(name="div", class_="FormattedHTMLContent_host__ZtwG0 Article_text__puPkY")
                data = {
                    "id": uuid.uuid4(),
                    "title": title,
                    "content": content,
                    "image": image.contents[0]['src'],
                    "url": link
                }
                response.append(data)

        for index, link in enumerate(data_science_urls_list):
            if index == 0:
                print("Link is", link)
                driver.get(link)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                title = soup.find(name="h1", class_="definition-title").string
                content = soup.find(name="section", class_="section definition-section")
                print("Content is", content.contents)
                image = soup.find(name="div", class_="image-trim")
                data = {
                    "id": uuid.uuid4(),
                    "title": title,
                    "content": "content",
                    "image": "image.contents[0]['src']",
                    "url": link
                }
                response.append(data)

        for index, link in enumerate(block_chain_urls_list):
            if index == 0:
                driver.get(link)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                title = soup.find(name="div",
                                  class_="clearfix text-formatted field field--name-field-p-body field--type-text-long field--label-hidden field__item")
                title_text = title.contents[1].contents[0]
                content = title.contents[3].contents[0]
                image = soup.find(name="figure", class_="caption caption-img")
                data = {
                    "id": uuid.uuid4(),
                    "title": title_text,
                    "content": content,
                    "image": "https:" + image.contents[0]['src'],
                    "url": link
                }
                response.append(data)

        for index, link in enumerate(vr_urls_list):
            if index == 0:
                driver.get(link)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                title = soup.find(name="h1",
                                  class_="headline")
                content = soup.find(name="p", class_="lead")
                data = {
                    "id": uuid.uuid4(),
                    "title": title.contents[0],
                    "content": content.contents[0],
                    "image": "",
                    "url": link
                }
                response.append(data)

        for index, link in enumerate(dev_ops_urls_list):
            if index == 0:
                driver.get(link)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                title = soup.find(name="h1", class_="article_bio-title")
                content = soup.find(name="p", class_="article_excerpt")
                data = {
                    "id": uuid.uuid4(),
                    "title": title.contents[0],
                    "content": content.contents[0],
                    "image": "",
                    "url": link
                }
                response.append(data)

        return Response(data={"success": "Articles have been scraped", "data": response}, status=status.HTTP_200_OK)

    except:
        return Response(data={"error": "Error while scraping articles"}, status=status.HTTP_400_BAD_REQUEST)
