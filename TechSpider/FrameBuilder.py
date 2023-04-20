import glob
import pathlib
from random import randint

import pandas
import pandas as pd
import time
import csv
import os
from bs4 import BeautifulSoup

folder_path = "gpu_specs"


def main():
    files = glob.glob(os.path.join(folder_path, '*.html'))
    for file_path in files:
        with open(file_path) as f:
            soup = BeautifulSoup(f, 'lxml')
            tables = soup.find_all("section", class_="details")
            try:
                card_name = soup.find("h1", class_="gpudb-name").text.strip()
            except:
                print(f"\033[1;31;40m re-scrape:{file_path} \033[0m 1;31;40m\n")
                continue
            table_graphics_card = find_heading_info("Graphics Card", ["Release Date", "Production"], soup, f)

            if table_graphics_card is None:
                table_graphics_card = find_heading_info("Integrated Graphics", ["Release Date", "Production"], soup, f)
            if table_graphics_card is None:
                table_graphics_card = find_heading_info("Mobile Graphics", ["Release Date", "Production"], soup, f)

            gp_table = find_heading_info("Graphics Processor", ["Foundry", "Process Size", "Transistors", "Die Size"],
                                         soup, f)
            board_design = find_heading_info("Board Design", ["Slot Width", "TDP"], soup, f)
            table_clock = find_heading_info("Clock Speeds", ["Base Clock", "Memory Clock"], soup, f)
            gpu_features = find_heading_info("Graphics Features",
                                             ["DirectX", "OpenGL", "OpenCL", "Vulkan", "CUDA", "Shader Model"], soup, f)
            tbl_memory = find_heading_info("Memory", ["Memory Size", "Memory Type", "Memory Bus", "Bandwidth"], soup, f)
            theory_tbl = find_heading_info("Theoretical Performance",["Pixel Rate","Texture Rate","FP16 (half)","FP32 (float)","FP64 (double)"],soup,f)
            print((card_name,file_path))
            print(gpu_features)
            print(tbl_memory)


def find_heading_info(heading, look_array, ref_soup, ref_file):
    tbl_elem = ref_soup.find('h2', string=lambda text: text.strip() == heading)
    if tbl_elem is None:
        print(f"\033[1;33;40m {heading} not found in: {ref_file}\x1b[0m\n")
    else:
        return find_in_heading(tbl_elem.parent, look_array)


def find_in_heading(element, look_array):
    output_arr = {}
    for element in element.find_all("dl"):
        for search in look_array:
            output_arr[search] = ""
            if element.find_all('dt')[0].text.strip() == search:
                output_arr[search] = element.find('dd').text.strip()
    return output_arr


if __name__ == '__main__':
    main()
