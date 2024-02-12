# import libraries
import csv
import re
import shutil
import time

import gzip
import ijson
# import requests

# def download_index_file(url: str, output_prefix: str) -> str:
#     """Download index file (gz) into data folder.
#     Args:
#         url (str): url string
#         output_prefix(str): output prefix
#     Returns:
#         str: output file path
#     """
#     file_path = f"{output_prefix}/{url.split('/')[-1]}"
#     with open(file_path, "wb") as f:
#         r = requests.get(url)
#         f.write(r.content)
#     return file_path


def decompress_gzip_to_json(input_file_path: str) -> str:
    """Decompress gzip to json file into data folder.

    Args:
        input_file_path (str): input file path ending in gz
        input_prefix (str): prefix for file path
    
    Returns:
        str: output file path ending in json
    """
    output_file_path = ".".join(input_file_path.split(".")[:-1])
    with gzip.open(input_file_path, "rb") as f_in:
        with open(output_file_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    return output_file_path


def get_url_set(input_file_path=str, plan_type=str, full_state=str, provider_name=str) -> set:
    """Get set of urls that match plan type, state, and provider.

    Args:
        input_file_path (str): input file path ending in json

    Returns:
        set: set of urls
    """
    url_set = set()
    with open(input_file_path, 'r') as file:
        # loop through every reporting structure iterator
        strm_struct = ijson.items(file, 'reporting_structure.item')        
        for struct_obj in strm_struct:

            # check if provider matches
            has_provider = False
            for plan_obj in struct_obj["reporting_plans"]:
                if 'plan_name' in plan_obj:
                    has_provider = bool(re.search(fr"\b{provider_name.lower()}\b", plan_obj['plan_name'].lower()))
                if has_provider:
                    break

            # if provider matches, check if state and plan type match
            if has_provider:
                for inn_obj in struct_obj['in_network_files']:
                    is_state = bool(re.search(fr"\b{full_state.lower()}\b", inn_obj['description'].lower()))
                    is_plan = bool(re.search(fr"\b{plan_type.lower()}\b", inn_obj['description'].lower()))
                    if is_state and is_plan:
                        url_set.add(inn_obj['location'])
    return url_set

def output_set_to_json(url_set: set, output_file_path: str) -> None:
    """Output set to json.

    Args:
        url_set (set): set of urls that match
        output_file_path (str): output file path
    """
    with open(output_file_path, "w") as file:
        wr = csv.writer(file, delimiter='\n')
        wr.writerow(list(url_set))
    return None


if __name__ == "__main__":
    # --- Set Variables ---
    # url = "https://antm-pt-prod-dataz-nogbd-nophi-us-east1.s3.amazonaws.com/anthem/2024-02-01_anthem_index.json.gz"
    plan_type = 'PPO'
    full_state = 'New York'
    provider_name = 'Anthem'
    gz_file_path = "data/2024-02-01_anthem_index.json.gz" # TODO: Move the zipped anthem file to the data folder
    output_file_path = "output/list_of_anthem_ny_ppo.csv"

    # --- Data Pipeline ---
    # gz_filename = download_index_file(url=url, output_prefix="data")
    time_0 = time.time()
    js_file_path = decompress_gzip_to_json(input_file_path=gz_file_path)
    time_1 = time.time()
    print(f"Step 0: Decompress File - Time(s): {time_1 - time_0}")
    url_set = get_url_set(input_file_path=js_file_path, plan_type=plan_type, full_state=full_state, provider_name=provider_name)
    time_2 = time.time()
    print(f"Step 1: Get URLs - Time(s): {time_2 - time_1}")
    output_set_to_json(url_set=url_set, output_file_path=output_file_path)
    time_3 = time.time()
    print(f"Step 2: Output to File - Time(s): {time_3 - time_2}")
    print(f"All Steps - Time(s): {time_3 - time_1}")
