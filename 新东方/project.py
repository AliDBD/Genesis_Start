#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/6/13 9:22
# @Author : Genesis Ai
# @File : project.py

import requests
from bs4 import BeautifulSoup
import os

# HTML content
html_content = '''<body class="file_link_main">
<div class="header_block">
    <div class="public_header">
        <div class="clearfix">
            <div class="pull-left mac_logo" style="height:32px">
                <a>
    <i class="gk_logo" style="background-image: url('http://dn-avatar.gokuai.com/4d/4dd8618a2b0506c1bf3ca65127ca9a8feeb80986.png')"></i>
</a>
            </div>
            <div class="pull-left mob_back">
                <a href="javascript:history.go(-1)" style="display: none;"></a>
            </div>
            <div class="pull-right dropdown user_button" style="margin-right: 12px;">
                                <div class="mac_menu">
                                                            <a href="https://yk3.gokuai.com/account/autologin/xdf?returnurl=/file/lbmro9nvmfw0c6f807bitgcktdcgaz60" class="link_login_btn">登录</a>
                                                        </div>
                
                <div class="mobile_menu">
                    <a href="javascript:;" class="username navbar-toggle" data-toggle="dropdown">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </a>

                    <ul class="dropdown-menu file_ops mobile_ops" role="menu">
                                                <li><a href="javascript:;" class="cmd_link_upload file-ops-btn" style="display: none;"><i class="link_upload"></i>上传</a></li>
                                                <li><a href="javascript:;" class="cmd_link_download" data-uri="/index/open_link_download?code=lbmro9nvmfw0c6f807bitgcktdcgaz60&amp;t=1718259201&amp;s=Lg%2F%2B1eSJdRsKP5OoAfVyYA776LM%3D" style="display: none;"><i class="link_download"></i>下载</a></li>
                                                <li>
                                                        <a href="https://yk3.gokuai.com/account/autologin/xdf?returnurl=/file/lbmro9nvmfw0c6f807bitgcktdcgaz60" class="cmd_save_link link_login_btn" style="display: none;"><i class="link_save"></i>保存到库</a>
                                                    </li>
                                                                                                <li style="border-bottom: 1px solid #e8e8e8;"><a href="javascript:;" class="cmd_send_link"><i class="link_email"></i>发送到邮箱</a></li>
                        
                                                <li><a href="javascript:;" data-display="list" class="toggle_display active"><i class="link_list"></i>列表模式</a></li>
                        <li><a href="javascript:;" data-display="thumb" class="toggle_display"><i class="link_thumb"></i>缩略图模式</a></li>
                        
                                                                        <li style="background-color: #f0f1f5;"><a href="https://yk3.gokuai.com/account/autologin/xdf?returnurl=/file/lbmro9nvmfw0c6f807bitgcktdcgaz60" class="link_login_btn">登录</a></li>
                                                
                                            </ul>
                </div>

            </div>

            <div class="pull-right clearfix desktop_ops mac_menu" style="margin-right: 12px;">
                                <button class="btn btn-primary cmd_link_upload file-ops-btn" style="display: none;">上传</button>
                                <div class="btn-group" role="group">
                    <button class="btn btn-primary cmd_link_download file-ops-btn" data-uri="/index/open_link_download?code=lbmro9nvmfw0c6f807bitgcktdcgaz60&amp;t=1718259201&amp;s=Lg%2F%2B1eSJdRsKP5OoAfVyYA776LM%3D" style="display: none;">下载</button>
                                        <button class="btn btn-primary dropdown-toggle cmd_link_download_caret file-ops-btn" data-toggle="dropdown" style="margin-left: 1px; display: none;"><i class="link_more"></i></button>
                    <ul class="dropdown-menu">
                                                <li class="cmd_save_link file-ops-btn" style="display: none;">
                                                        <a href="https://yk3.gokuai.com/account/autologin/xdf?returnurl=/file/lbmro9nvmfw0c6f807bitgcktdcgaz60" class="link_login_btn">保存到库</a>
                                                    </li>
                                            </ul>
                </div>
            </div>
        </div>
        <div class="link_name">
            <span>
            <span class="true_font">【2】2022年绿宝书解析：拱墅+上城+西湖+滨江+钱塘</span>
                <a href="javascript:;" style="display: inline-block;">
                    <i></i>

                    <div class="link_information">
                        <ul>
                            <li><label>文件名称：</label><span>【2】2022年绿宝书解析：拱墅+上城+西湖+滨江+钱塘</span></li>
                                                        <li><label>分享者：</label><span>吕晓彤</span></li>
                                                        <li><label>失效时间：</label><span>2024/06/30 23:59</span></li>
                                                    </ul>
                    </div>
                </a>
            </span>
        </div>
    </div>
</div>
<div class="link_block" style="padding-bottom:0;">
    <div class="file_link_dialog mount_file_main">
        <div class="file_bread">
            <div class="file_bread_btns pull-right">
                <button class="btn btn-primary link_list_sort file-ops-btn" style="">按时间排序                    <span class="sort"><s class="arrow-top"></s><s class="arrow-bottom"></s></span>
                </button>
                <div class="btn-group switch" role="group">
                    <button type="button" data-display="list" class="btn btn-primary toggle_display file-ops-btn active" style="display: block;"><i class="list"></i></button>
                    <button type="button" data-display="thumb" class="btn btn-primary toggle_display file-ops-btn" style="display: block;"><i class="thumb"></i></button>
                </div>
            </div>
            <ol class="breadcrumb"><li><a href="javascript:;" title="【2】2022年绿宝书解析：拱墅+上城+西湖+滨江+钱塘">【2】2022年绿宝书解析：拱墅+上城+西湖+滨江+钱塘</a></li></ol>
        </div>
        <div class="file_body">
            <div class="file_content">
                <div class="file_main"><div class="table-body scrollbar" style="top:0">
<table class="file_list table">
    <thead>
    <tr>
        <th width="68"></th>
        <th></th>
        <th style="min-width:140px;width:20%"></th>
        <th style="min-width:140px;width:20%"></th>
    </tr>
    </thead>
    <tbody>
                                    <tr class="file_item" data-icon="icon_document icon_pdf" data-filename="1-1【2022】【六下】【拱墅区】【分班考】【语文】解析.pdf" data-dir="0" data-fullpath="1-1【2022】【六下】【拱墅区】【分班考】【语文】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:41" data-size="0.89MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="1-1【2022】【六下】【拱墅区】【分班考】【语文】解析.pdf">1-1【2022】【六下】【拱墅区】【分班考】【语文】解析.pdf</a>
            </td>
    <td>2023-11-21 14:15</td>
    <td>0.89MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="1-2【2022】【六下】【拱墅区】【分班考】【数学】解析.pdf" data-dir="0" data-fullpath="1-2【2022】【六下】【拱墅区】【分班考】【数学】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:40" data-size="0.46MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="1-2【2022】【六下】【拱墅区】【分班考】【数学】解析.pdf">1-2【2022】【六下】【拱墅区】【分班考】【数学】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>0.46MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="1-3【2022】【六下】【拱墅区】【分班考】【英语】解析.pdf" data-dir="0" data-fullpath="1-3【2022】【六下】【拱墅区】【分班考】【英语】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:39" data-size="0.39MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="1-3【2022】【六下】【拱墅区】【分班考】【英语】解析.pdf">1-3【2022】【六下】【拱墅区】【分班考】【英语】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>0.39MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="1-4【2022】【六下】【拱墅区】【分班考】【科学】解析.pdf" data-dir="0" data-fullpath="1-4【2022】【六下】【拱墅区】【分班考】【科学】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:39" data-size="0.59MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="1-4【2022】【六下】【拱墅区】【分班考】【科学】解析.pdf">1-4【2022】【六下】【拱墅区】【分班考】【科学】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>0.59MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="2-1【2022】【六下】【上城区】【分班考】【语文】解析.pdf" data-dir="0" data-fullpath="2-1【2022】【六下】【上城区】【分班考】【语文】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:39" data-size="0.74MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="2-1【2022】【六下】【上城区】【分班考】【语文】解析.pdf">2-1【2022】【六下】【上城区】【分班考】【语文】解析.pdf</a>
            </td>
    <td>2023-05-30 10:33</td>
    <td>0.74MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="2-2【2022】【六下】【上城区】【分班考】【数学】解析.pdf" data-dir="0" data-fullpath="2-2【2022】【六下】【上城区】【分班考】【数学】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:37" data-size="0.67MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="2-2【2022】【六下】【上城区】【分班考】【数学】解析.pdf">2-2【2022】【六下】【上城区】【分班考】【数学】解析.pdf</a>
            </td>
    <td>2023-03-17 10:49</td>
    <td>0.67MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="2-3【2022】【六下】【上城区】【分班考】【英语】解析.pdf" data-dir="0" data-fullpath="2-3【2022】【六下】【上城区】【分班考】【英语】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:36" data-size="0.2MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="2-3【2022】【六下】【上城区】【分班考】【英语】解析.pdf">2-3【2022】【六下】【上城区】【分班考】【英语】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>0.2MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="2-4【2022】【六下】【上城区】【分班考】【科学】解析.pdf" data-dir="0" data-fullpath="2-4【2022】【六下】【上城区】【分班考】【科学】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:37" data-size="0.91MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="2-4【2022】【六下】【上城区】【分班考】【科学】解析.pdf">2-4【2022】【六下】【上城区】【分班考】【科学】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>0.91MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="3-1【2022】【六下】【西湖区】【分班考】【语文】解析.pdf" data-dir="0" data-fullpath="3-1【2022】【六下】【西湖区】【分班考】【语文】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:35" data-size="0.58MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="3-1【2022】【六下】【西湖区】【分班考】【语文】解析.pdf">3-1【2022】【六下】【西湖区】【分班考】【语文】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>0.58MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="3-2【2022】【六下】【西湖区】【分班考】【数学】解析.pdf" data-dir="0" data-fullpath="3-2【2022】【六下】【西湖区】【分班考】【数学】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:35" data-size="0.79MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="3-2【2022】【六下】【西湖区】【分班考】【数学】解析.pdf">3-2【2022】【六下】【西湖区】【分班考】【数学】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>0.79MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="3-3【2022】【六下】【西湖区】【分班考】【英语】解析.pdf" data-dir="0" data-fullpath="3-3【2022】【六下】【西湖区】【分班考】【英语】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:34" data-size="1.03MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="3-3【2022】【六下】【西湖区】【分班考】【英语】解析.pdf">3-3【2022】【六下】【西湖区】【分班考】【英语】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>1.03MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="3-4【2022】【六下】【西湖区】【分班考】【科学】解析.pdf" data-dir="0" data-fullpath="3-4【2022】【六下】【西湖区】【分班考】【科学】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:31" data-size="0.71MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="3-4【2022】【六下】【西湖区】【分班考】【科学】解析.pdf">3-4【2022】【六下】【西湖区】【分班考】【科学】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>0.71MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="4-1【2022】【六下】【滨江区】【分班考】【语文】解析.pdf" data-dir="0" data-fullpath="4-1【2022】【六下】【滨江区】【分班考】【语文】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:32" data-size="1.05MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="4-1【2022】【六下】【滨江区】【分班考】【语文】解析.pdf">4-1【2022】【六下】【滨江区】【分班考】【语文】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>1.05MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="4-2【2022】【六下】【滨江区】【分班考】【数学】解析.pdf" data-dir="0" data-fullpath="4-2【2022】【六下】【滨江区】【分班考】【数学】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:30" data-size="0.93MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="4-2【2022】【六下】【滨江区】【分班考】【数学】解析.pdf">4-2【2022】【六下】【滨江区】【分班考】【数学】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>0.93MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="4-3【2022】【六下】【滨江区】【分班考】【英语】解析.pdf" data-dir="0" data-fullpath="4-3【2022】【六下】【滨江区】【分班考】【英语】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:28" data-size="0.18MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="4-3【2022】【六下】【滨江区】【分班考】【英语】解析.pdf">4-3【2022】【六下】【滨江区】【分班考】【英语】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>0.18MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="4-4【2022】【六下】【滨江区】【分班考】【科学】解析.pdf" data-dir="0" data-fullpath="4-4【2022】【六下】【滨江区】【分班考】【科学】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:28" data-size="0.59MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="4-4【2022】【六下】【滨江区】【分班考】【科学】解析.pdf">4-4【2022】【六下】【滨江区】【分班考】【科学】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>0.59MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="5-1【2022】【六下】【钱塘区】【分班考】【语文】解析.pdf" data-dir="0" data-fullpath="5-1【2022】【六下】【钱塘区】【分班考】【语文】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:27" data-size="0.71MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="5-1【2022】【六下】【钱塘区】【分班考】【语文】解析.pdf">5-1【2022】【六下】【钱塘区】【分班考】【语文】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>0.71MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="5-2【2022】【六下】【钱塘区】【分班考】【数学】解析.pdf" data-dir="0" data-fullpath="5-2【2022】【六下】【钱塘区】【分班考】【数学】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:27" data-size="1.01MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="5-2【2022】【六下】【钱塘区】【分班考】【数学】解析.pdf">5-2【2022】【六下】【钱塘区】【分班考】【数学】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>1.01MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="5-3【2022】【六下】【钱塘区】【分班考】【英语】解析.pdf" data-dir="0" data-fullpath="5-3【2022】【六下】【钱塘区】【分班考】【英语】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:24" data-size="0.3MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="5-3【2022】【六下】【钱塘区】【分班考】【英语】解析.pdf">5-3【2022】【六下】【钱塘区】【分班考】【英语】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>0.3MB</td>
</tr><tr class="file_item" data-icon="icon_document icon_pdf" data-filename="5-4【2022】【六下】【钱塘区】【分班考】【科学】解析.pdf" data-dir="0" data-fullpath="5-4【2022】【六下】【钱塘区】【分班考】【科学】解析.pdf" data-create_member="吕晓彤" data-create_dateline="2023/03/17 10:17:28" data-size="1.74MB" data-jump="" data-permission="">
    <td><i class="file_icon icon_document icon_pdf">
                
            </i></td>
    <td>
                <a href="javascript:;" class="file_name" title="5-4【2022】【六下】【钱塘区】【分班考】【科学】解析.pdf">5-4【2022】【六下】【钱塘区】【分班考】【科学】解析.pdf</a>
            </td>
    <td>2023-03-17 10:17</td>
    <td>1.74MB</td>
</tr>                            </tbody>
</table>
</div></div>
            </div>
        </div>
    </div>
</div>
<script id="dlg" type="text/x-jquery-tmpl">
<div class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog ${dialogClass}">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                <h4 class="modal-title" id="myModalLabel">${title}</h4>
            </div>
            <div class="modal-body">

            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-primary ${okClass}">确认</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">取消</button>
            </div>
        </div>
    </div>
</div>
</script>
<script id="editNameTmpl" type="text/x-jquery-tmpl">
<span class="edit_name">
    <span class="col-xs-{{if showBtn}}5{{else}}12{{/if}}">
        <input class="form-control new_name" type="text" value="${oldname}" x-webkit-speech="" {{if maxLength}}maxlength="${maxLength}" {{/if}}/>
    </span>
    <span class="col-xs-7 {{if !showBtn}}hide{{/if}}" >
        <button class="btn btn-primary save_name" >确定</button>
        <button class="btn btn-default cancel_edit">取消</button>
    </span>
</span>
</script>
<script id="showIframeDialog" type="text/x-jquery-tmpl">
<div class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog iframe_dialog ${dialogClass}" {{if width}}style="width:${width}px"{{/if}} >
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                <h4 class="modal-title" id="myModalLabel">${title}</h4>
            </div>
            <div class="modal-body">
                <iframe src="${uri}" class="scrollbar" width="100%" frameborder="0" height="{{if height}}${height}{{else}}550{{/if}}"></iframe>
            </div>
        </div>
    </div>
</div>
</script>
<script id="showLaunchDialog" type="text/x-jquery-tmpl">
<div class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog launch_dialog"  >
        <div class="modal-content">
            <div class="modal-body">
                <h2>欢迎使用</h2>
                <p>网页版仅提供最基本的功能，体验完整的功能请使用客户端</p>
                <div class='continue_use'><a href='javascript:;' >继续使用网页版</a></div>
                <div class="clearfix not_pop">
                    <label class="pull-right"><input type="checkbox" />下次不再提醒</label>
                </div>
            </div>
        </div>
    </div>
</div>
</script>

<script id="sendMailTmpl" type="text/x-jquery-tmpl">
<div class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                <h4 class="modal-title" id="myModalLabel">发送到邮箱</h4>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <input type="email" class="form-control" id="mail" placeholder="请输入邮箱地址">
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-primary" id="send_btn" data-loading-text="正在发送...">发送</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">取消</button>
            </div>
        </div>
    </div>
</div>
</script>
<noscript>
    <meta http-equiv="refresh" content="0;url=/index/noscript">
</noscript>
<script type="text/javascript" src="/Static/js/common/jquery.js?v=1.12.4"></script>
<script type="text/javascript" src="/Static/js/common/jquery-ui.js?v=1.11.4"></script>
<script type="text/javascript" src="/Static/js/common/jquery.tmpl.min.js?v=1.0.0"></script>
<script type="text/javascript" src="/Static/js/common/jquery.cookie.js?v=1.0.0"></script>
<script type="text/javascript" src="/Static/js/common/jsMD5.js"></script>
<script type="text/javascript" src="/Static/js/common/base64.min.js"></script>

<!--<script type="text/javascript" src="/Static/js/common/json2.js"></script>-->
<!--<script type="text/javascript" src="/Static/js/common/zeroclipboard/dist/ZeroClipboard.min.js?v=2.1.6"></script>-->
<script type="text/javascript" src="/Static/js/common/jquery.mousewheel.js?v=3.1.6"></script>
<script type="text/javascript" src="/Static/js/common/jquery.event.move.js?v=1.3.6"></script>
<script type="text/javascript" src="/Static/js/common/jquery.event.swipe.js?v=1.2"></script>
<script type="text/javascript" src="/Static/js/common/nprogress/nprogress.js?v=0.2"></script>

<script type="text/javascript" src="/index/langjs?v=1692093458&amp;lang=zh-cn" charset="UTF-8"></script>
<script type="text/javascript" src="/Static/js/lang/zh-cn.js?v=1692093458"></script>

<script type="text/javascript" src="/Static/bootstrap/js/bootstrap.js?v=3.0.1"></script>
<script type="text/javascript" src="/Static/bootstrap/touchspin/bootstrap.touchspin.js?v=2.8.0"></script>

<script type="text/javascript" src="/Static/js/lib/util.js?v=1692093458"></script>

<script type="text/javascript" src="/Static/js/component/loader.js?v=1692093458"></script>
<script type="text/javascript" src="/Static/js/component/alert.js?v=1692093458"></script>
<script type="text/javascript" src="/Static/js/component/scrollLoad.js?v=1692093458"></script>

<script type="text/javascript" src="/Static/js/lib/common.js?v=1692093458"></script>
<script type="text/javascript" src="/Static/js/lib/file.js?v=1692093458"></script>
<script type="text/javascript" src="/Static/js/ajax.js?v=1692093458"></script>
<script type="text/javascript" src="/Static/js/account.js?v=1692093458"></script>
<script type="text/javascript" src="/Static/js/mount.js?v=1692093458"></script>
<script type="text/javascript" src="/Static/js/index.js?v=1692093458"></script>
<script type="text/javascript" src="/Static/js/common/pwstrength.js?v=1692093458"></script>
<!-- Deploy -->
<script type="text/javascript" src="/Deploy/script.js?v=1692093458"></script>

<script id="showLoginDialog" type="text/x-jquery-tmpl">
<div class="modal" tabindex="-1" role="dialog" data-backdrop="static">
    <div class="modal-dialog login_info_dialog" >
        <div class="modal-content">
            <div class="modal-body">
                <h3>请在新打开的页面认证登录</h3>
                <a class="btn btn-primary" href="javascript:location.reload();">我已登录</a>
                                <div>或&nbsp;<a href='https://passport.gokuai.com/account/login' target="_blank">使用帐号密码登录</a></div>
                            </div>
        </div>
    </div>
</div>
</script>
<script type="text/javascript">
    var newLoginWindow = "";
    $(function () {
        window.loginCallback = function(win){
            win.close();
            location.reload();
        };
        if (newLoginWindow) {
            $('.link_login_btn').prop('target', '_blank').on('click', function () {
                gkAccount.login.showInfo()
            });
        }
    });
</script>
<script type="text/javascript">
    $(function () {
        gkFiles.link.outer.init({
            site_domain: "yk3.gokuai.com",
            dir: "1",
            code: "lbmro9nvmfw0c6f807bitgcktdcgaz60",
            mount_id: "789914",
            is_login: "",
            deadline: "1719763140",
            dateline: "1718259201",
            is_owner: "",
            sign: "Lg/+1eSJdRsKP5OoAfVyYA776LM=",
            preview: "1",
            login_prefix: '',
            lvu: '/index/link_visit?code=lbmro9nvmfw0c6f807bitgcktdcgaz60&dateline=1718259201&sign=Lg%2F%2B1eSJdRsKP5OoAfVyYA776LM%3D',
            upload_url: ''
        });
    })
</script>

</body>'''

# Parse HTML
soup = BeautifulSoup(html_content, 'html.parser')
tbody = soup.find('tbody')

# Extract filenames
filenames = [tr['data-filename'] for tr in tbody.find_all('tr', class_='file_item')]

# Base URL
base_url = 'https://yk3.gokuai.com/file/lbmro9nvmfw0c6f807bitgcktdcgaz60#!::'

# Directory to save PDF files
save_dir = 'downloaded_pdfs'

# Create directory if it doesn't exist
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


# Function to download file with retries
def download_file(url, file_path, retries=3):
    for i in range(retries):
        try:
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            # Check if file was downloaded correctly
            if os.path.getsize(file_path) > 0:
                return True
        except Exception as e:
            print(f'Error downloading {url}: {e}')
        print(f'Retrying {url}... ({i + 1}/{retries})')
    return False


# Download PDF files
for filename in filenames:
    pdf_url = f'{base_url}{filename}:'
    print(f'Downloading {pdf_url}')

    file_path = os.path.join(save_dir, filename)
    if download_file(pdf_url, file_path):
        print(f'Successfully downloaded {filename} to {file_path}')
    else:
        print(f'Failed to download {filename}')

print('Download completed.')
