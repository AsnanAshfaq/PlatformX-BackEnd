from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

artificial_urls_list = [
    {
        "link": "https://www.brookings.edu/research/how-artificial-intelligence-is-transforming-the-world/",
    },
    {
        "link": "https://futureoflife.org/background/benefits-risks-of-artificial-intelligence/?cn-reloaded=1"
    }

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
        for index, key in enumerate(artificial_urls_list):
            if index == 0:
                driver.get(key["link"])
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                title = soup.find(name="h1", class_="report-title").string
                content = soup.find(name="div", class_="summary-text").p.string
                image = soup.source['srcset']
                data = {
                    "id": 1,
                    "title": title,
                    "content": content,
                    "image": image,
                    "url": key["link"]
                }
                response.append(data)
            # if index == 1:
            #     driver.get(key["link"])
            #     soup = BeautifulSoup(driver.page_source, 'html.parser')
            #     titleTag = soup.find(name="h1", class_="av-special-heading-tag")
            #     title = titleTag.contents[0].string + titleTag.contents[1].string + titleTag.contents[2].string
            #     content = soup.find(name="div", class_="avia_textblock").contents[0]
            #     print("Content is", content)
            #     # content = soup.find(name="div", class_="avia_textblock").p.string
            #     # imageTag = soup.find(name="div", class_="avia-image-overlay-wrap").image
            #     # print("Image tag is", imageTag)
            #     # image = imageTag['src']
            #     data = {
            #         "id": 1,
            #         "title": title,
            #         "content": "content",
            #         "image": "image",
            #         "url": key["link"]
            #     }
            #     response.append(data)

        return Response(data={"success": "Articles have been scraped", "data": response}, status=status.HTTP_200_OK)

    except:
        return Response(data={"error": "Error while scraping articles"}, status=status.HTTP_400_BAD_REQUEST)
