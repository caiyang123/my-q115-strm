from p115client import P115Client
from server import LibSync, LIBS
from lib import OO5List
import argparse
import sys
import time
from datetime import datetime

if __name__ == '__main__':
    key: str = ''
    parser = argparse.ArgumentParser(prog='115-STRM', description='将挂载的115网盘目录生成STRM',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-k', '--key', help='要处理的同步目录')
    args, unknown = parser.parse_known_args()
    print(args)
    if args.key != None:
        key = args.key
    if key == '':
        sys.exit(0)

    print(f"key: {key}")

    libItem = LIBS.getLib(key)
    print(f"libItem: {libItem}")
    if libItem is None:
        sys.exit(0)

    print(f"last_sync_at: {libItem.extra.last_sync_at}")
    date_obj = time.strptime(libItem.extra.last_sync_at, "%Y-%m-%d %H:%M:%S")
    start_time = int(time.mktime(date_obj))
    print(f"start_time: {start_time}")

    end_time = datetime.now().timestamp()
    print(f"end_time: {end_time}")

    oo5List = OO5List()
    oo5Item = oo5List.get(libItem.id_of_115)
    print(f"cookie: {oo5Item.cookie}")
    client = P115Client(oo5Item.cookie)
    life_list = client.life_list({"start_time": start_time, 'end_time': end_time})
    notify = False
    for item in life_list["data"]["list"]:
        if item["behavior_type"] in ("receive_files", "move_file"):
            print(f"item: {item}")
            notify = True
            break
        if item["behavior_type"] == "delete_file":
            if "_目录树.txt" not in item["items"][0]["file_name"]:
                notify = True
                break

    print(f"notify: {notify}")
    if notify:
        libSync = LibSync()
        libSync.post(libItem.key)