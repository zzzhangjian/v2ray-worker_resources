import zipfile
import os
import requests


zip_url = "https://zip.baipiao.eu.org/"
ports = ["80", "443"]


def download_and_extract():
    # Step 1: Download the zip file
    response = requests.get(zip_url)
    zip_file_path = "download.zip"

    with open(zip_file_path, "wb") as file:
        file.write(response.content)

    # Step 2: Extract the files from the zip
    extracted_files_dir = "./extracted_files/"
    os.makedirs(extracted_files_dir, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extracted_files_dir)

    # Step 3: Combine the text files into one file
    combined_file_path = "ips.txt"

    with open(combined_file_path, "w") as combined_file:
        for root, dirs, files in os.walk(extracted_files_dir):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    for i in ports:
                        if '-'+i+'.' in file:
                            with open(file_path, "r") as txt_file:
                                combined_file.write(txt_file.read())
    # Step 4: Open combined_file_path,Print the contents of the combined file
    # 假设 combined_file_path 已经定义为你想要读取的文件路径
    rows = []
    with open(combined_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            print(line.strip())  # 使用 strip() 方法去除每行末尾的换行符
            response = requests.get(f'http://ip-api.com/json/{line.strip()}?lang=zh-CN')
            print(response)
            if response.ok:
                res = response.json()
                print(res)
            rows.append(f'{line.strip()},{res["country"]}-{res["regionName"]}-{res["city"]}')
    with open(combined_file_path, 'w', encoding='utf-8') as file:
        for line in rows:
            file.write(line + '\n')
    # with open(combined_file_path, "w") as combined_file:
    #     lines = combined_file.readlines()
    #     for line in lines:
    #         print(line)
    #         response = requests.get(f'http://ip-api.com/json/{line}?lang=zh-CN')
    #         if response.code == 200:
    #             res = response.json()
    #             print(res)
    
download_and_extract()
