import os
import requests
from bs4 import BeautifulSoup
print("Script Started")
os.makedirs('One Piece', exist_ok=True)
os.chdir("One Piece")

def get_image(url, folder_name, file_name):
    data = requests.get(url)
    os.makedirs(folder_name, exist_ok=True)
    with open(os.path.join(folder_name, file_name), "wb") as write_file:
        for chunk in data.iter_content(10000000):
            write_file.write(chunk)

for i in range(1, 12):
    data_url = f"https://w60.1piecemanga.com/manga/one-piece-chapter-{i}/"
    print(f"Chapter {i}")
    soup = BeautifulSoup(requests.get(data_url).text, "html.parser")
    # Get the image url and name from each chapter page?
    images = soup.find_all("img")
    for j in range(0, len(images)):
        image_url = images[j]["src"]
        print(f"Image {j}")

        folder_name = f"Chapter_{i}"
        file_name = f"page_{j}.png"
        get_image(image_url, folder_name, file_name)