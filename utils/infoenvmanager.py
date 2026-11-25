import os
from dotenv import load_dotenv

from function import get_app_root_dir
from network import download_coco2017_ndjson
from logger import *

root_dir = get_app_root_dir()
env_path = root_dir / ".env"
load_dotenv(dotenv_path=env_path)
USERNAME = os.getenv("USERNAME")
API_KEYS = os.getenv("API_KEYS")

def update_coco2017_ndjson(output_path: str = f"{root_dir}/pdata/coco2017.ndjson"):
    outcome = download_coco2017_ndjson(
        api_key=API_KEYS,
        owner="ultralytics",
        dataset="coco2017",
        output_path=output_path,
    )
    print("结果:", outcome["message"])

    # 如果需要排查问题，完整的导出响应始终保存在 outcome["export_response"] 中
    if not outcome["ok"]:
        print("导出接口状态码:", outcome["export_response"]["status_code"])
        print("导出接口 body:", outcome["export_response"]["body"])
