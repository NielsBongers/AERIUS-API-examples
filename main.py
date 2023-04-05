import time 
import shutil 
import logging 
import requests
from pathlib import Path 

def get_logger(logger_name): 
    Path("Logs").mkdir(parents=True, exist_ok=True) 
    
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s.%(msecs)03d [%(levelname)s] [%(name)s] %(message)s", 
        datefmt = "%d-%m-%Y %H:%M:%S", 
        handlers=[
            logging.FileHandler("logs/file.log", mode="a"),
            logging.StreamHandler()
    ]
    )
    
    return logging.getLogger(logger_name)


def upload_gml(gml_file_name, api_key): 
    headers = {
        'accept': 'application/json',
        'api-key': api_key,
    }

    files = {
        'options': (None, '{"name": "string","calculationYear": 2023,"sendEmail": true,"outputType": "GML","calculationPointsType": "WNB_RECEPTORS","receptorSetName": "string","appendices": [  "EDGE_EFFECT_REPORT"]\n}'),
        'files': (None, '[{"fileName": "' + gml_file_name + '","situation": "REFERENCE","groupId": 0,"substance": "NH3","calculationYear": 2023\n}]'),
        'fileParts': open(Path("GML", gml_file_name), 'rb')
    }

    response = requests.post('https://connect.aerius.nl/api/v7/wnb/calculate', headers=headers, files=files).json()

    job_key = response["jobKey"]
    
    return job_key 


def get_status(job_key, api_key): 
    headers = {
        'accept': 'application/json',
        'api-key': api_key,
    }

    response = requests.get('https://connect.aerius.nl/api/v7/jobs/' + job_key, headers=headers).json() 
    status = response["status"]

    return status 
    
def download_result(job_key, api_key, file_dest): 
    headers = {
        'accept': 'application/json',
        'api-key': api_key,
    }

    response = requests.get('https://connect.aerius.nl/api/v7/jobs/' + job_key, headers=headers).json() 
    file_url = response["resultUrl"]

    with requests.get(file_url, stream=True) as r:
        with open(Path("Reports", file_dest), 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
            
def main(): 
    logger = get_logger(__name__) 
    api_key = "f57c690b4cbf476684047f3293a0ac13" 
    gml_file = "test2.gml" 
    file_dest = "output.zip"
    
    logger.info(f"Sending {gml_file}.")
    job_key = upload_gml(gml_file, api_key) 
    logger.info(f"Job key: {job_key}.")

    while True: 
        status = get_status(job_key, api_key) 
        logger.info(f"Current reported status is: {status.lower()}.")
        
        if status == "COMPLETED": 
            break
    
        time.sleep(1) 

    logger.info(f"Downloading results to {Path('Reports', file_dest)}.")
    download_result(job_key, api_key, file_dest) 
        
    
    
    
    
if __name__ == "__main__": 
    main() 