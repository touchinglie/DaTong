import os
from dotenv import load_dotenv

from utils.function import get_app_root_dir
from utils.network import download_coco2017_ndjson

env_path = get_app_root_dir() / ".env"

print(env_path)

load_dotenv(dotenv_path=env_path)

USERNAME = os.getenv("USERNAME")
API_KEYS = os.getenv("API_KEYS")

print("USERNAME:", USERNAME)
print("API_KEYS:", API_KEYS)

outcome = download_coco2017_ndjson(
       api_key=API_KEYS,
       owner="ultralytics",
       dataset="coco2017",
       output_path="test/coco2017.ndjson",
   )

print("结果:", outcome["message"])

# 如果需要排查问题，完整的导出响应始终保存在 outcome["export_response"] 中
if not outcome["ok"]:
    print("导出接口状态码:", outcome["export_response"]["status_code"])
    print("导出接口 body:", outcome["export_response"]["body"])