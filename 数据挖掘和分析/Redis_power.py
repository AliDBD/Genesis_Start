#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/6/26 8:35
# @Author : Genesis Ai
# @File : redes.py

import redis
import time

# 定义 redis1 和 redis 主机信息
redis1_host = '172.18.3.157'
redis1_port = 6379
redis1_db = 7
redis1_password = 'am0C4$TieX'

redis2_host = '172.18.3.232'
redis2_port = 6379
redis2_db = 15
redis2_password = 'ZFgmP2ev'

# 连接 redis1 和 redis2 并验证密码
redis1 = redis.StrictRedis(host=redis1_host, port=redis1_port, db=redis1_db, password=redis1_password)
redis2 = redis.StrictRedis(host=redis2_host, port=redis2_port, db=redis2_db, password=redis2_password)

# 设置每次批量迁移的数据量
batch_size = 1000

# 为进度跟踪初始化变量
keys_processed = 0
start_time = time.time()

# 使用 SCAN 批量获取 key
cursor = '0'
total_keys = len(redis1.keys('com:cg:growth:*'))

while cursor != 0:
    cursor, keys = redis1.scan(cursor, count=batch_size)
    for key in keys:
        key_data = redis1.dump(key)
        redis2.restore(key, 0, key_data, replace=True)

        keys_processed += 1

        # 每 1000 个 key 打印一次进度
        if keys_processed % batch_size == 0 or keys_processed == total_keys:
            elapsed_time = time.time() - start_time
            keys_per_second = batch_size / elapsed_time
            estimated_remaining_time = (total_keys - keys_processed) / keys_per_second

            print(f"Processed {keys_processed}/{total_keys} keys. "
                  f"Elapsed Time: {elapsed_time:.2f} seconds. "
                  f"Estimated Remaining Time: {estimated_remaining_time:.2f} seconds for the next 1000 keys.")

            # 为下一批次重置变量
            start_time = time.time()

print("Data migration completed.")