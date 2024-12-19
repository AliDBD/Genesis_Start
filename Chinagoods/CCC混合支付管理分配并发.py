#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/12/16 16:14
# @Author : Genesis Ai
# @File : CCC混合支付管理分配并发.py

import asyncio
import aiohttp
import datetime
import json

# 配置请求的基本信息
API_URL = "https://testapiserver.chinagoods.com/sms/admin/v1/shopMixedServicePayment/distribute"
TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsicmVzb3VyY2VPbmUiXSwidXNlcl9uYW1lIjp7ImxvZ2luVHlwZSI6ImFkbWluU21zIiwiaXNBZG1pbiI6dHJ1ZSwibG9naW5OYW1lIjoiMTM3OTk5OTk5OTkiLCJuZXdNYXJrZXRJZHMiOiIxMSw0NCw5OSwwMSwxMiwwMiwxMyw0NiwwMyw0NywwNCw0OCwwNSw0OSwwNiwwNywwOCwwOSw1MCw1MSwxMCIsInd4VXNlcklkIjoiIiwiZ2VuZGVyIjoiTSIsImRlbCI6Ik4iLCJtYXJrZXRJZHMiOiI0NDUwLDQ0NTEsMTAxMSwxMDA4LDEwMDcsMTAwNiwxMDA1LDEwMDQsMTAwMywxMDE0LDEwMDIsMTAxMywxMDAxLDEwMTIsNDQ0NCw0NDQ2LDk5OTksNDQ0Nyw0NDQ4LDQ0NDksMTAwOSIsInByaXZpbGVnZSI6IlMiLCJzaG9ydFBob25lIjoiIiwidXNlck5hbWUiOiLnrqHnkIblkZgiLCJyYW5rSWRMaXN0IjpbIkNISU5BX0dPT0RTX1NZU19TVVBFUl9VU0VSIl0sImxhc3RMb2dpblRpbWUiOiIyMDI0LTEyLTE2VDE1OjUxOjI5IiwicmVhbE5hbWUiOiLnrqHnkIblkZgiLCJtb2RpZnlUaW1lIjoiMjAyNC0xMi0xNlQxNTo1MToyOSIsInBvc2l0aW9uSWQiOjIsImNyZWF0ZVRpbWUiOiIyMDIwLTA3LTI4VDE1OjQyOjI4IiwicGFzc3dkIjoiJDJhJDEwJDh6TDkwMW1lTHV5dW5rd01JSnhIOWVtWlBFZGJGVEVocnRVb3QwTEpoVFBNMUlXcEFHdjFhIiwicGhvbmUiOiIxMzc5OTk5OTk5OSIsImFwcElkIjoiQ0hJTkFfR09PRFMiLCJsb2dvIjoiIiwic2VsZiI6Ik4iLCJpZCI6NDF9LCJzY29wZSI6WyJBRE1JTiJdLCJleHAiOjE3MzQ0MDc0OTEsImF1dGhvcml0aWVzIjpbIkNISU5BX0dPT0RTX1NZU19TVVBFUl9VU0VSIl0sImp0aSI6ImM4ZTY5YTFhLTQ5NjEtNDBiNS05ODQ3LWU0MTllMzU3MzQ1OCIsImNsaWVudF9pZCI6ImFkbWluIn0.tMYrrlkmmyKQIIc1sH0UpSn8Nn6cf30_zCsX-crTAu9yi68xM_orNOp4NV58Rhxz9YvAUd3AXijgtwUVgsAWMWww8VpOfrJGcACqheHVfuznHsLk6dpt3JyCaYKUsDkhQs2KZs2f9iqUvpZjEEIgL0HJuzLpwLO25ktpf8Wb7obVkEtquvKR8i5RrDEXl90hUOt9fQGe3_9ZLHdPwAWyLsUVcOjh663lkxmGjRlUKTL6BvU_0ZyU_41SdB3OOIieJINQnbnW9gW0QKN8MBhHflptmSpRhWoOdXQ8Cb84v1724mhPFZfNNV6XNj7Mymfdcm-U3mdK2qlrp-9CnErIvA"  # 请填完整
HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}
PAYLOAD_TEMPLATE = {
    "shopId": 53196,
    "shopName": "大荒漠土特产旗舰店",
    "lang": "zh",
    "orderNo": "",  # 这个字段会动态替换
    "saleMan": "0319",
    "saleManId": "41",
    "payAmount": 180000,
    "payTime": "",  # 动态设置
    "remark": "",
    "dataSource": 1,
    "sortCode": 0,
    "marketAdminOperatorId": 327,
    "marketAdminName": "陈钢林/国际商贸城一区",
    "marketAdminTelephone": "13867927078",
    "operatorSource": 1,
    "marketName": "国际商贸城一区",
    "payType": 1,
    "distributionStatus": 1,
    "attachmentsUrl": "[]",
    "remainPayAmount": 180000,
    "contacts": "林靖宇",
    "telephone": "13408400153",
    "content": "无",
    "shopVipPayAmount": 0
}

# 生成动态orderNo列表
ORDER_NO_LIST = [
    "MIXEDPAY20241216164653938476",
    "MIXEDPAY20241216164709724036",
    "MIXEDPAY20241216164719099138",
    "MIXEDPAY20241216164725926506"
]


async def send_request(session, order_no, request_id, order_index):
    """发送单个请求"""
    payload = PAYLOAD_TEMPLATE.copy()
    payload["id"] = str(44 + order_index)
    payload["orderNo"] = order_no
    payload["payTime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        async with session.post(API_URL, headers=HEADERS, json=payload) as response:
            resp_text = await response.text()
            print("\n" + "="*50)
            print(f"订单号: {order_no}")
            print(f"请求ID: {request_id}")
            print(f"订单序号: {order_index + 1}")
            print(f"payload id: {payload['id']}")
            print(f"状态码: {response.status}")
            print("响应内容:")
            try:
                resp_json = json.loads(resp_text)
                print(json.dumps(resp_json, indent=2, ensure_ascii=False))
            except:
                print(resp_text)
            print("="*50 + "\n")
    except Exception as e:
        print(f"订单号 {order_no} (请求ID: {request_id}) 请求失败: {str(e)}")


async def process_single_order(session, order_no, order_index, concurrent_requests=15):
    """处理单个订单的多个并发请求"""
    tasks = []
    for i in range(concurrent_requests):
        task = send_request(session, order_no, f"并发请求-{i+1}", order_index)
        tasks.append(task)
    await asyncio.gather(*tasks)


async def run_concurrent_requests():
    """运行并发请求，每个订单模拟多人同时请求"""
    connector = aiohttp.TCPConnector(limit=10)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        for index, order_no in enumerate(ORDER_NO_LIST):
            print(f"\n开始处理订单: {order_no}")
            await process_single_order(session, order_no, index, concurrent_requests=15)
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(run_concurrent_requests())
        print("所有请求处理完成")
    except Exception as e:
        print(f"程序执行错误: {e}")
