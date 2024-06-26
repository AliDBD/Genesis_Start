#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/5/11 10:16
# @Author : Genesis Ai
# @File : test.py


#方法1
# import yfinance as yf  # 用于获取股票数据的库
# import smtplib  # 用于发送邮件的库
# from email.mime.multipart import MIMEMultipart  # 构建多部分邮件
# from email.mime.text import MIMEText  # 构建邮件正文
# from email.utils import formatdate  # 格式化日期
# import os  # 用于文件和路径操作

# 股票代码和中文名称的映射
# stock_info = {
#     "600415.SS": "小商品城",
#     "600988.SS": "赤峰黄金",
#     "002142.SZ": "宁波银行",
#     "002497.SZ": "雅化集团"
# }
#
# def get_stock_info(ticker):
#     """
#     获取指定股票的当天开盘价、收盘价及涨跌幅度
#     :param ticker: 股票代码，例如 '600415.SS' 表示小商品城
#     :return: 包含股票代码、中文名称、开盘价、收盘价和涨跌幅度的字典或 None（如果无法获取数据）
#     """
#     stock = yf.Ticker(ticker)  # 创建一个 Ticker 对象
#     data = stock.history(period="1d")  # 获取最近一天的历史数据
#     if not data.empty:
#         open_price = data['Open'].iloc[0]  # 提取开盘价格
#         close_price = data['Close'].iloc[0]  # 提取收盘价格
#         change = close_price - open_price  # 计算涨跌幅度
#         return {
#             "ticker": ticker,
#             "name": stock_info.get(ticker, "未知公司"),
#             "open": open_price,
#             "close": close_price,
#             "change": change
#         }
#     else:
#         return None
#
# def send_email(sender_email, sender_password, recipient_emails, subject, body):
#     """
#     发送邮件
#     :param sender_email: 发送方邮箱
#     :param sender_password: 发送方邮箱密码
#     :param recipient_emails: 收件人邮箱列表
#     :param subject: 邮件主题
#     :param body: 邮件正文
#     """
#     # 创建邮件对象
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = ", ".join(recipient_emails)
#     msg['Date'] = formatdate(localtime=True)
#     msg['Subject'] = subject
#
#     # 添加邮件正文，指定编码为 utf-8 以处理中文字符
#     msg.attach(MIMEText(body, 'plain', 'utf-8'))
#
#     # 连接到SMTP服务器并发送邮件
#     try:
#         server = smtplib.SMTP('smtp.163.com', 587)
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.sendmail(sender_email, recipient_emails, msg.as_string())
#         server.quit()
#         print("Email sent successfully!")
#     except Exception as e:
#         print(f"Failed to send email: {e}")
#
# if __name__ == "__main__":
#     # 示例使用
#     sender_email = "linjingyu1031@163.com"
#     sender_password = "PWEYDSPLPFPASVQH"
#     recipient_emails = [
#         "linjingyu@chinagoods.com"
#     ]
#
#     # 要获取信息的股票代码列表
#     stock_tickers = ["600415.SS", "600988.SS", "002142.SZ", "002497.SZ"]
#
#     # 邮件主题
#     subject = "Daily Stock Report"
#
#     # 构建邮件正文
#     body = "今日股票信息:\n\n"
#     for ticker in stock_tickers:
#         info = get_stock_info(ticker)
#         if info:
#             body += (f"股票代码: {info['ticker']}\n"
#                      f"股票名称: {info['name']}\n"
#                      f"开盘价格: {info['open']:.2f}\n"
#                      f"收盘价格: {info['close']:.2f}\n"
#                      f"涨跌幅度: {info['change']:.2f}\n\n")
#         else:
#             body += f"无法获取股票代码为 {ticker} 的信息\n\n"
#
#     # 发送邮件
#     send_email(sender_email, sender_password, recipient_emails, subject, body)


#方法2
import yfinance as yf  # 用于获取股票数据的库
import smtplib  # 用于发送邮件的库
from email.mime.multipart import MIMEMultipart  # 构建多部分邮件
from email.mime.text import MIMEText  # 构建邮件正文
from email.utils import formatdate  # 格式化日期

# 股票代码和中文名称的映射
stock_info = {
    "600415.SS": "小商品城",
    "600988.SS": "赤峰黄金",
    "002142.SZ": "宁波银行",
    "002497.SZ": "雅化集团",
    "300750.SZ": "宁德时代",
    "002236.SZ": "大华股份",
    "600685.SS": "中船防务"
}

def get_stock_info(ticker):
    """
    获取指定股票的当天开盘价、收盘价及涨跌幅度
    :param ticker: 股票代码，例如 '600415.SS' 表示小商品城
    :return: 包含股票代码、中文名称、开盘价、收盘价和涨跌幅度的字典或 None（如果无法获取数据）
    """
    stock = yf.Ticker(ticker)  # 创建一个 Ticker 对象
    data = stock.history(period="1d")  # 获取最近一天的历史数据
    if not data.empty:
        open_price = data['Open'].iloc[0]  # 提取开盘价格
        close_price = data['Close'].iloc[0]  # 提取收盘价格
        change = close_price - open_price  # 计算涨跌幅度
        return {
            "ticker": ticker,
            "name": stock_info.get(ticker, "未知公司"),
            "open": open_price,
            "close": close_price,
            "change": change
        }
    else:
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
        # 连接到SMTP服务器并发送邮件
        server = smtplib.SMTP_SSL('smtp.163.com', 465)
        server.set_debuglevel(1)  # 启用调试输出
        server.ehlo("localhost")
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_emails, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # 示例使用
    sender_email = "linjingyu1031@163.com"
    sender_password = "PWEYDSPLPFPASVQH"
    recipient_emails = [
        "2316248267@qq.com",
        "1076881630@qq.com"
    ]

    # 要获取信息的股票代码列表
    stock_tickers = ["600415.SS", "600988.SS", "002142.SZ", "002497.SZ", "300750.SZ", "002236.SZ", "600685.SS"]

    # 邮件主题
    subject = "Daily Stock Report"

    # 构建邮件正文
    body = "今日股票信息:\n\n"
    for ticker in stock_tickers:
        info = get_stock_info(ticker)
        if info:
            body += (f"股票代码: {info['ticker']}\n"
                     f"股票名称: {info['name']}\n"
                     f"开盘价格: {info['open']:.2f}元\n"
                     f"收盘价格: {info['close']:.2f}元\n"
                     f"涨跌幅度: {info['change']:.2f}%\n\n")
        else:
            body += f"无法获取股票代码为 {ticker} 的信息\n\n"

    # 发送邮件
    send_email(sender_email, sender_password, recipient_emails, subject, body)
