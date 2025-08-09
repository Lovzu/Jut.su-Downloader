import requests
from bs4 import BeautifulSoup as bs
import fake_useragent
from tqdm import tqdm
import re
import os
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)
logger = logging.getLogger(__name__)

class DownloadAnime:
    def __init__(self, url, quality, save_path, chunk_size=65536):
        self.url = url
        self.quality = quality
        self.save_path = save_path
        self.chunk_size = chunk_size
        self.session = requests.Session()
        user_agent = fake_useragent.UserAgent().random
        self.session.headers.update({"User-Agent": user_agent})
        logging.warning(f"Inputs: \nURL: {url},\nQuality:{quality}, \nSave Path: {save_path}, \nChunk size: {chunk_size}")

    def validate_inputs(self):
        logging.warning("Starting function validate_inputs")
        if all([self.quality, self.save_path]):
            quality = str(re.search(r'\d+', self.quality).group()) + 'p'
            logging.warning(f"Quality anime: {quality}")
            save_path = os.path.normpath(self.save_path) + os.sep
            logging.warning(f'Save path: {save_path}')
            return quality, save_path

    def get_request(self):
        logging.warning("Starting function get_request")
        quality, save_path = self.validate_inputs()
        logging.warning(f'Get request to {self.url}')
        response = self.session.get(self.url)
        response.raise_for_status()
        soup = bs(response.text, "lxml")
        pleer_url = soup.find_all("source", label=quality)[0]['src']
        logging.warning(f"Pleer url: {pleer_url}")
        file_name = soup.find('span', itemprop="name").get_text(strip=True)[8:] + '.mp4'
        file_name = file_name if file_name else 'video.mp4'
        logging.warning(f'Anime name: {file_name}')
        save_path = os.path.join(save_path, file_name)
        logging.warning(f"Full directory save path: {save_path}")
        return pleer_url, save_path

    def download(self):
        pleer_url, save_path = self.get_request()
        headers = {
            "Referer": self.url,
            "Range": "bytes=0-"
        }
        logging.warning(f"Start downloading from {pleer_url}")
        with self.session.get(pleer_url, headers=headers, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            logging.warning(f"Total size: {total_size}")
            with open(save_path, "wb") as f, tqdm(
                desc='Downloading',
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024
            ) as bar:
                for chunk in r.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        size = f.write(chunk)
                        bar.update(size)
        logging.warning('Download Successfully!')

pattern = r'^https://jut\.su/([a-z-]+)/season-(\d+)/episode-(\d+)\.html$'
qualities = [720, 1080, 480]

url = input('Please, input jut.su anime url: ')
match = re.match(pattern, url)
if match is None:
    raise Exception("Wrong URL")

quality = input('What quality want you?(1080, 720, 480): ')

if int(re.search(r'\d+', quality).group()) not in qualities:
    raise Exception("Wrong quality")
save_directory_path = input("Input your directory to save anime(without filename): ")

download_anime = DownloadAnime(url, quality, save_directory_path)
download_anime.download()
