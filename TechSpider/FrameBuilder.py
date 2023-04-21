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
    df = pd.DataFrame()
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

            gp_table = find_heading_info("Graphics Processor", ["Foundry", "Process Size", "Transistors", "Die Size",
                                                                "Architecture"],
                                         soup, f)
            if table_graphics_card is None and gp_table is not None:
                table_graphics_card = {"Release Date": find_heading_info("Graphics Processor",
                                                                         ["Released"],
                                                                         soup, f)["Released"],
                                       "Production": ""}
            board_design = find_heading_info("Board Design", ["Slot Width", "TDP"], soup, f)
            table_clock = find_heading_info("Clock Speeds", ["Base Clock", "Memory Clock"], soup, f)
            gpu_features = find_heading_info("Graphics Features",
                                             ["DirectX", "OpenGL", "OpenCL", "Vulkan", "CUDA", "Shader Model"], soup, f)
            tbl_memory = find_heading_info("Memory", ["Memory Size", "Memory Type", "Memory Bus", "Bandwidth"], soup, f)
            theory_tbl = find_heading_info("Theoretical Performance",
                                           ["Pixel Rate", "Texture Rate", "FP16 (half)", "FP32 (float)",
                                            "FP64 (double)"], soup, f)
            rndr_config_tbl = find_heading_info("Render Config",
                                                ["Shading Units", "Max. TDP"], soup, f)
            print(table_graphics_card)
            dicst = {"card_name": card_name,
                     "foundry": gp_table["Foundry"] if gp_table is not None else None,
                     "process_size": gp_table["Process Size"] if gp_table is not None else None,
                     "transistors": gp_table["Transistors"] if gp_table is not None else None,
                     "die_size": gp_table["Die Size"] if gp_table is not None else None,
                     "architecture": gp_table["Architecture"] if gp_table is not None else None,
                     "slot_width": board_design["Slot Width"] if board_design is not None else None,
                     "tdp": board_design["TDP"] if board_design is not None else None,
                     "base_clock": table_clock["Base Clock"] if table_clock is not None else None,
                     "mem_clock": table_clock["Memory Clock"] if table_clock is not None else None,
                     "directX_ver": gpu_features["DirectX"] if gpu_features is not None else None,
                     "opengl_ver": gpu_features["OpenGL"] if gpu_features is not None else None,
                     "opencl_ver": gpu_features["OpenCL"] if gpu_features is not None else None,
                     "vulkan_ver": gpu_features["Vulkan"] if gpu_features is not None else None,
                     "cuda_ver": gpu_features["CUDA"] if gpu_features is not None else None,
                     "shader_model_ver": gpu_features["Shader Model"] if gpu_features is not None else None,
                     "mem_size": tbl_memory["Memory Size"] if tbl_memory is not None else None,
                     "mem_type": tbl_memory["Memory Type"] if tbl_memory is not None else None,
                     "mem_bus": tbl_memory["Memory Bus"] if tbl_memory is not None else None,
                     "bandwidth": tbl_memory["Bandwidth"] if tbl_memory is not None else None,
                     "pixel_rate": theory_tbl["Pixel Rate"] if theory_tbl is not None else None,
                     "texture_rate": theory_tbl["Texture Rate"] if theory_tbl is not None else None,
                     "FP16_rate": theory_tbl["FP16 (half)"] if theory_tbl is not None else None,
                     "FP32_rate": theory_tbl["FP32 (float)"] if theory_tbl is not None else None,
                     "FP64_rate": theory_tbl["FP64 (double)"] if theory_tbl is not None else None,
                     "shading_units": rndr_config_tbl["Shading Units"] if rndr_config_tbl is not None else None,
                     "production_status": table_graphics_card[
                         "Production"] if table_graphics_card is not None else None,
                     "release_date": table_graphics_card["Release Date"] if table_graphics_card is not None else None,
                     }
            df = df.append(dicst, ignore_index=True)

    df.to_csv("gpu-data.csv")


def find_heading_info(heading, look_array, ref_soup, ref_file):
    tbl_elem = ref_soup.find('h2', string=lambda text: text.strip() == heading)
    if tbl_elem is None:
        print(f"\033[1;33;40m {heading} not found in: {ref_file}\x1b[0m\n")
    else:
        return find_in_heading(tbl_elem.parent, look_array)


def find_in_heading(element, look_array):
    output_arr = {}
    for temp in look_array:
        output_arr[temp] = ""
    for dl in element.find_all("dl"):
        for dt in dl.find_all('dt'):
            dt_text = dt.text.strip()
            if dt_text in look_array:
                dd_text = dl.find('dd').text.strip()
                output_arr[dt_text] = dd_text
    return output_arr


if __name__ == '__main__':
    main()
