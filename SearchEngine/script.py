import os
import datetime
import json
import time

from model import extract

path = r"../media/dataset"

external_url = r"https://archive.org/download/TOIDELFEB18/TOIDEL-FEB-18.zip/02%2F"
internal_url = r"http://localhost:8000/media/dataset/"
delimeter = ","
count = 0
start = time.time()


with open('data.json', 'w') as file:
    file.write("[")
    for date in os.listdir(path):
        print(date)

        for news_image in os.listdir(path + "/" + date):
            if not news_image.endswith("C.png"):
                continue

            print(news_image)

            if count != 0:
                file.write(delimeter)

            e_url = external_url + f"{date}" + "%2F" + news_image
            i_url = internal_url + "/" + date + "/" + news_image

            extracted_text = extract(i_url)

            news_data = {
                "model": "accounts.NewsRecord",
                "fields": {
                    "file_path": i_url,
                    "external_file_path": e_url,
                    "extracted_text": extracted_text,
                    "timestamp": str(datetime.datetime.now())
                }
            }

            json.dump(news_data, file)

            count += 1

    file.write("]")

end = time.time()

required_time = end - start

day = required_time // (24 * 3600)
required_time = required_time % (24 * 3600)

hour = required_time // 3600
required_time %= 3600

minutes = required_time // 60
required_time %= 60

seconds = required_time

print("d:h:m:s -> %d:%d:%d:%d" % (day, hour, minutes, seconds))
print("Total records:", count)


# Script to load data in model
# python manage.py loaddata searchengine/data.json
