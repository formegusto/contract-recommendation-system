from utils import *
import sys
import requests as req


@update_process("reco-process-start")
def start():
    return


if __name__ == "__main__":
    file_name = sys.argv[1]

    start()

    xlsx = load_excel(file_name)

    # p, m = data_preprocessing(xlsx)
    # req.patch(api_server + update_path, json={
    #     "type": "data-preprocessing",
    #     "status": True
    # })
