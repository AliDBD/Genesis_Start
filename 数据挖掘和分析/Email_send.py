#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/5/17 8:54
# @Author : Genesis Ai
# @File : Email_send.py

import yfinance as yf  # 用于获取股票数据的库
import smtplib  # 用于发送邮件的库
from email.mime.multipart import MIMEMultipart  # 构建多部分邮件
from email.mime.text import MIMEText  # 构建邮件正文
from email.utils import formatdate  # 格式化日期
import time  # 用于添加延时
import json  # 用于缓存数据
import socket  # 用于检查网络连接
import os  # 用于设置工作目录
import logging  # 用于日志记录
from datetime import datetime  # 用于获取当前时间

# 配置日志记录
logging.basicConfig(filename='E:\\untitled\\spider\\数据挖掘和分析\\stock_report.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 股票代码和中文名称的映射
stock_info = {
    "600415.SS": "小商品城",
    "600988.SS": "赤峰黄金",
    "002142.SZ": "宁波银行",
    "002497.SZ": "雅化集团",
    "002459.SZ": "晶澳科技",
    "300750.SZ": "宁德时代",
    "002236.SZ": "大华股份",
    "600685.SS": "中船防务"
}

# 缓存文件名
cache_file = 'E:\\2024年\\python_for_temp\\stock_cache.json'

def clear_cache():
    """清空缓存文件"""
    if os.path.exists(cache_file):
        os.remove(cache_file)
        logging.info("Cache file removed.")

def load_cache():
    """从缓存文件加载数据"""
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.info("Cache file not found, starting with an empty cache.")
        return {}

def save_cache(cache):
    """将数据保存到缓存文件"""
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=4)
        logging.info("Cache saved successfully.")

def check_network():
    """检查网络连接"""
    try:
        socket.create_connection(("www.baidu.com", 80))
        logging.info("Network is available.")
        return True
    except OSError:
        logging.error("Network is not available.")
        return False

def get_stock_info(ticker, retries=3, delay=5):
    """
    获取指定股票的当天开盘价、收盘价及涨跌幅度
    :param ticker: 股票代码，例如 '600415.SS' 表示小商品城
    :param retries: 失败重试次数
    :param delay: 重试延迟时间（秒）
    :return: 包含股票代码、中文名称、开盘价、收盘价和涨跌幅度的字典或 None（如果无法获取数据）
    """
    for attempt in range(retries):
        try:
            logging.info(f"Fetching data for {ticker}, attempt {attempt + 1}/{retries}")
            stock = yf.Ticker(ticker)  # 创建一个 Ticker 对象
            data = stock.history(period="1d")  # 获取最近一天的历史数据
            logging.debug(f"Raw data for {ticker}: {data}")
            if not data.empty:
                open_price = data['Open'].iloc[0]  # 提取开盘价格
                close_price = data['Close'].iloc[0]  # 提取收盘价格
                change = close_price - open_price  # 计算涨跌幅度
                stock_data = {
                    "ticker": ticker,
                    "name": stock_info.get(ticker, "未知公司"),
                    "open": open_price,
                    "close": close_price,
                    "change": change
                }
                logging.info(f"Successfully fetched data for {ticker}")
                return stock_data
            else:
                logging.warning(f"No data found for {ticker}")
        except Exception as e:
            logging.error(f"Failed to get data for {ticker}, attempt {attempt + 1}/{retries}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
    return None

def send_email(sender_email, sender_password, recipient_emails, subject, body):
    """
    发送邮件
    :param sender_email: 发送方邮箱
    :param sender_password: 发送方邮箱密码
    :param recipient_emails: 收件人邮箱列表
    :param subject: 邮件主题
    :param body: 邮件正文
    """
    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_emails)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    # 添加邮件正文，指定编码为 utf-8 以处理中文字符
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        logging.info("Connecting to SMTP server...")
        # 连接到SMTP服务器并发送邮件
        server = smtplib.SMTP_SSL('smtp.163.com', 465)
        server.set_debuglevel(1)  # 启用调试输出
        server.ehlo("localhost")
        logging.info("Logging in to SMTP server...")
        server.login(sender_email, sender_password)
        logging.info("Sending email...")
        server.sendmail(sender_email, recipient_emails, msg.as_string())
        server.quit()
        logging.info("Email sent successfully!")
    except smtplib.SMTPException as e:
        logging.error(f"Failed to send email: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    # 设置工作目录为脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    logging.info("Script started")

    # 检查网络连接
    if not check_network():
        logging.error("Network is not available")
        exit(1)

    # 清空缓存
    clear_cache()

    # 示例使用
    sender_email = "linjingyu1031@163.com"
    sender_password = "PWEYDSPLPFPASVQH"
    recipient_emails = [
        "2316248267@qq.com",
        "1076881630@qq.com",
        "870344926@qq.com",
        "linjingyulove@gmail.com"
    ]

    # 要获取信息的股票代码列表
    stock_tickers = ["600415.SS", "600988.SS", "002142.SZ", "002497.SZ","002459.SZ", "300750.SZ", "002236.SZ", "600685.SS"]

    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 邮件主题
    subject = "Daily closing consultation"

    # 构建邮件正文
    body = f"代码执行时间：{current_time}\n\n今日股票信息:\n\n"
    for ticker in stock_tickers:
        info = get_stock_info(ticker)
        logging.debug(f"Fetched info for {ticker}: {info}")
        if info:
            body += (f"股票代码: {info['ticker']}\n"
                     f"股票名称: {info['name']}\n"
                     f"开盘价格: {info['open']:.2f}￥\n"
                     f"收盘价格: {info['close']:.2f}￥\n"
                     f"涨跌幅度: {info['change']:.2f}%\n\n")
        else:
            body += f"无法获取股票代码为 {ticker} 的信息\n\n"

    logging.debug(f"Final email body: {body}")

    # 发送邮件
    send_email(sender_email, sender_password, recipient_emails, subject, body)

    logging.info("Script finished")
