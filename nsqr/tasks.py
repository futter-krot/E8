from urllib.error import URLError
from urllib.request import urlopen
from celery import shared_task
from bs4 import BeautifulSoup
import re
from time import sleep


@shared_task(bind=True)
def findpy(self, url):
    word = "python"
    try:
        html = urlopen(url).read()
    except URLError:
        return -1
    soup = BeautifulSoup(html, features="html.parser")

    for script in soup(["script", "style"]):
        script.decompose()

    results = soup.body.find_all(string=re.compile('.*{0}.*'.format(word)), recursive=True)
    return len(results)
