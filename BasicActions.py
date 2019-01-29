from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException, NoSuchElementException, NoSuchWindowException, TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from spoofmac.util import random_mac_address
from spoofmac.interface import set_interface_mac
import mysql.connector
from sshtunnel import SSHTunnelForwarder
from multiprocessing import Queue
import Tkinter as tk
import ttk
import time
import os
import threading
import re
import SocketServer
from random import randint

root = tk.Tk()
mac = tk.BooleanVar()
mac_wt = tk.IntVar()
ua = tk.StringVar()
prt = tk.StringVar()
box_val = tk.StringVar()
wtf1 = tk.IntVar()
wtf2 = tk.IntVar()
wts1 = tk.IntVar()
wts2 = tk.IntVar()
wtc1 = tk.IntVar()
wtc2 = tk.IntVar()
wtm = tk.IntVar()
site = tk.StringVar()


class BasicActions(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        frame = tk.Frame(root)

        with SSHTunnelForwarder(
                ("cloudhost.kr", 22),
                ssh_password="nvandh0327^^",
                ssh_username="root",
                remote_bind_address=("127.0.0.1", 3306)
        ) as tunnel:
            conn = mysql.connector.connect(user="cloudhos_auth",
                                           password="venEv5gwdcQ5",
                                           host="127.0.0.1",
                                           port=tunnel.local_bind_port,
                                           database="cloudhos_auth")

            cursor = conn.cursor()
            cursor.execute("SELECT category FROM nrs_target_keyword")
            result = cursor.fetchall()
            categories = list()
            for row in result:
                categories.append(row[0])

            cursor.close()
            conn.close()

        left_lf = tk.LabelFrame(root, text="")
        right_lf = tk.LabelFrame(root, text="")
        # IP change label, radiobutton
        mac_lb = tk.Label(root, text="""Change IP""")
        mac_rb1 = tk.Radiobutton(root, text="Yes", variable=mac, value=1)
        mac_rb1.select()
        mac_rb2 = tk.Radiobutton(root, text="No", variable=mac, value=2)

        # Browser selection label, radiobutton
        ua_lb = tk.Label(root, text="""Select Browser""")
        ua_rb1 = tk.Radiobutton(root, text="IE 10", variable=ua, value="ff")
        ua_rb1.select()
        ua_rb2 = tk.Radiobutton(root, text="IE 11", variable=ua, value="ch")
        ua_rb3 = tk.Radiobutton(root, text="Random", variable=ua, value="rn")

        # Portal selection label, radiobutton
        prt_lb = tk.Label(root, text="""Select Portal""")
        prt_rb1 = tk.Radiobutton(root, text="Naver", variable=prt, value="naver")
        prt_rb1.select()
        prt_rb2 = tk.Radiobutton(root, text="Daum", variable=prt, value="daum")

        # Keyword label, select box
        kw_lb = tk.Label(root, text="""Select Keyword""")
        kw_sb = ttk.Combobox(root, textvariable=box_val)
        kw_sb["values"] = categories
        kw_sb.current(0)
        kw_sb.bind("<<ComboboxSelected>>")

        # Waiting period on first page
        wt1_lb1 = tk.Label(root, text="""Waiting Period (First Page)""")
        wt1_ent1 = tk.Entry(root, textvariable=wtf1)
        wt1_lb2 = tk.Label(root, text="""/s""")
        wt1_ent2 = tk.Entry(root, textvariable=wtf2)
        wt1_lb3 = tk.Label(root, text="""/s""")

        # Waiting period after typing and clicking search button
        wt2_lb1 = tk.Label(root, text="""Waiting Period (After Search)""")
        wt2_ent1 = tk.Entry(root, textvariable=wts1)
        wt2_lb2 = tk.Label(root, text="""/s""")
        wt2_ent2 = tk.Entry(root, textvariable=wts2)
        wt2_lb3 = tk.Label(root, text="""/s""")

        # Waiting period after click
        wt3_lb1 = tk.Label(root, text="""Waiting Period (After Click)""")
        wt3_ent1 = tk.Entry(root, textvariable=wtc1)
        wt3_lb2 = tk.Label(root, text="""/s""")
        wt3_ent2 = tk.Entry(root, textvariable=wtc2)
        wt3_lb3 = tk.Label(root, text="""/s""")

        # Waiting period main
        wt4_lb1 = tk.Label(root, text="""How many cycles""")
        wt4_ent2 = tk.Entry(root, textvariable=wtm)

        # Start button
        btn = tk.Button(root, text="Start", command=self.setup)

        # Layout settings
        frame.grid(columnspan=7, rowspan=8, sticky=(tk.N, tk.S, tk.E, tk.W), padx=10, pady=10)
        left_lf.grid(in_=frame, column=0, row=0, sticky=(tk.W, tk.N, tk.S, tk.W), padx=15, pady=15)
        right_lf.grid(in_=frame, column=1, row=0, sticky=(tk.E, tk.N, tk.S, tk.W), padx=15, pady=15)
        # IP
        mac_lb.grid(in_=left_lf, column=0, row=0, padx=5, pady=5, sticky=tk.W)
        mac_rb1.grid(in_=left_lf, column=1, row=0, sticky=tk.W)
        mac_rb2.grid(in_=left_lf, column=2, row=0, sticky=tk.W)
        # Browser
        ua_lb.grid(in_=left_lf, column=0, row=2, padx=5, pady=5, sticky=tk.W)
        ua_rb1.grid(in_=left_lf, column=1, row=2, sticky=tk.W)
        ua_rb2.grid(in_=left_lf, column=2, row=2, sticky=tk.W)
        ua_rb3.grid(in_=left_lf, column=3, row=2, sticky=tk.W)
        # Portal
        prt_lb.grid(in_=left_lf, column=0, row=3, padx=5, pady=5, sticky=tk.W)
        prt_rb1.grid(in_=left_lf, column=1, row=3, sticky=tk.W)
        prt_rb2.grid(in_=left_lf, column=2, row=3, sticky=tk.W)
        # Keyword
        kw_lb.grid(in_=left_lf, column=0, row=4, padx=5, pady=15, sticky=tk.W)
        kw_sb.grid(in_=left_lf, column=1, row=4, padx=5, pady=15)
        # Period 1
        wt1_lb1.grid(in_=right_lf, column=3, row=0, padx=5, sticky=tk.W)
        wt1_lb2.grid(in_=right_lf, column=4, row=1)
        wt1_lb3.grid(in_=right_lf, column=6, row=1, padx=5)
        wt1_ent1.grid(in_=right_lf, column=3, row=1, padx=5, pady=5)
        wt1_ent2.grid(in_=right_lf, column=5, row=1, padx=5, pady=5)
        # Period 2
        wt2_lb1.grid(in_=right_lf, column=3, row=2, padx=5, sticky=tk.W)
        wt2_lb2.grid(in_=right_lf, column=4, row=3)
        wt2_lb3.grid(in_=right_lf, column=6, row=3)
        wt2_ent1.grid(in_=right_lf, column=3, row=3, padx=5, pady=5)
        wt2_ent2.grid(in_=right_lf, column=5, row=3, padx=5, pady=5)
        # Period 3
        wt3_lb1.grid(in_=right_lf, column=3, row=4, padx=5, sticky=tk.W)
        wt3_lb2.grid(in_=right_lf, column=4, row=5)
        wt3_lb3.grid(in_=right_lf, column=6, row=5)
        wt3_ent1.grid(in_=right_lf, column=3, row=5, padx=5, pady=5)
        wt3_ent2.grid(in_=right_lf, column=5, row=5, padx=5, pady=5)
        # Period 4
        wt4_lb1.grid(in_=right_lf, column=3, row=6, padx=5, sticky=tk.W)
        wt4_ent2.grid(in_=right_lf, column=3, row=7, padx=5, pady=15)
        # Start
        btn.grid(column=3, row=8, pady=10, padx=10)

    def setup(self):
        browser = ua.get()
        portal = prt.get()
        ip_yn = mac.get()
        wp_ip = mac_wt.get()
        wp1s = wtf1.get()
        wp1e = wtf2.get()
        wp2s = wts1.get()
        wp2e = wts2.get()
        wp3s = wtc1.get()
        wp3e = wtc2.get()
        wp4s = wtm.get()
        sel_val = box_val.get()
        global site
        options = Options()

        for i in range(wp4s):
            if browser == "ff":
                options.add_argument("user-agent=Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)")
            elif browser == "ch":
                options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko")
            else:
                uas = ["user-agent=Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)",
                       "user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0",
                       "user-agent=Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Win64; x64; Trident/6.0)",
                       "user-agent=Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.151 Safari/534.16",
                       "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"]

                print uas[randint(0, len(uas))]
                options.add_argument(uas[randint(0, len(uas))])

            if portal == "naver":
                site = "http://www.naver.com/"
            elif portal == "daum":
                site = "http://www.daum.net/"

            with SSHTunnelForwarder(
                    ("cloudhost.kr", 22),
                    ssh_password="nvandh0327^^",
                    ssh_username="root",
                    remote_bind_address=("127.0.0.1", 3306)
            ) as tunnel:
                conn = mysql.connector.connect(user="cloudhos_auth",
                                               password="venEv5gwdcQ5",
                                               host="127.0.0.1",
                                               port=tunnel.local_bind_port,
                                               database="cloudhos_auth")

                cursor = conn.cursor()
                cursor.execute("SELECT keyword FROM nrs_target_keyword WHERE category = '%s'" % sel_val)
                keyword = cursor.fetchall()
                str_key = ""
                for k in keyword:
                    str_key = k[0]

                str_key = str(str_key.encode("utf-8"))
                str_arr = str_key.split("<BR>")
                for s in str_arr:
                    self.driver = webdriver.Chrome(chrome_options=options)
                    self.driver.get(site)
                    time.sleep(randint(wp1s, wp1e))
                    self.test_scroll(randint(wp2s, wp2e))
                    self.test_random_click(randint(wp3s, wp3e))
                    self.test_scroll(randint(wp3s, wp3e))
                    self.test_go_back()
                    s_arr = s.split(",")
                    for j in s_arr:
                        time.sleep(5)
                        self.test_do_search(j.decode("utf-8"))
                        self.test_scroll(randint(5, 10))
                        self.test_search_click(randint(wp3s, wp3e))
                        self.test_scroll(randint(5, 10))
                        self.test_search_back()
                        time.sleep(5)
                    self.tear_down()
                    if ip_yn:
                        self.change_ip()
                    else:
                        pass

                cursor.close()
                conn.close()
                time.sleep(120)

    def change_ip(self):
        os.chdir("C:\Program Files (x86)\Technitium\TMACv6.0")
        os.system("tmac -n Ethernet -r -re -s")

    def test_scroll(self, t):
        time.sleep(t)
        driver = self.driver
        cnt = 0
        for i in range(100):
            cnt += i
            driver.execute_script("window.scrollBy(0, %s)" % i)
            time.sleep(0.1)

        if cnt > 0:
            for i in range(100):
                driver.execute_script("window.scrollBy(0, -%s)" % i)
                time.sleep(0.1)

    def test_random_click(self, t):
        time.sleep(t)
        global site
        driver = self.driver
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, "")))
        links = driver.find_elements_by_partial_link_text("")

        while True:
            try:
                if driver.current_url == site:
                    link = links[randint(0, len(links) - 1)]
                    link.click()
                    time.sleep(5)
                    if driver.current_url != site:
                        break
                else:
                    continue
            except:
                continue

    def test_search_click(self, t):
        time.sleep(t)
        global site
        driver = self.driver
        if driver.find_elements_by_class_name("question"):
            links = driver.find_elements_by_class_name("question")
        elif driver.find_elements_by_class_name("sh_blog_title"):
            links = driver.find_elements_by_class_name("sh_blog_title")
        elif driver.find_elements_by_class_name("_sp_each_url"):
            links = driver.find_elements_by_class_name("_sp_each_url")
        elif driver.find_elements_by_class_name("sh_cafe_title"):
            links = driver.find_elements_by_class_name("sh_cafe_title")

        while True:
            try:
                cur_windows = driver.window_handles
                link = links[randint(0, len(links) - 1)]
                link.click()
                if len(cur_windows) >= 1:
                    break
                else:
                    continue
            except (ElementNotVisibleException, StaleElementReferenceException, TimeoutException):
                continue

    def test_go_back(self):
        driver = self.driver
        origin_win = driver.current_window_handle
        cur_windows = driver.window_handles

        for win in cur_windows:
            if win != origin_win and len(cur_windows) > 1:
                driver.switch_to.window(win)
                driver.close()
            else:
                driver.back()

        driver.switch_to.window(origin_win)

    def test_search_back(self):
        driver = self.driver
        origin_win = driver.current_window_handle
        cur_windows = driver.window_handles

        for win in cur_windows:
            if win != origin_win and len(cur_windows) > 1:
                driver.switch_to.window(win)
                driver.close()
            elif win == origin_win and len(cur_windows) == 1:
                driver.back()

        driver.switch_to.window(origin_win)

    def test_do_search(self, query):
        driver = self.driver
        try:
            if driver.find_element_by_name("query").is_displayed():
                driver.find_element_by_name("query").clear()
                driver.find_element_by_name("query").send_keys(query)

            if driver.find_element_by_id("search_btn").is_displayed():
                driver.find_element_by_id("search_btn").click()
            elif driver.find_element_by_class_name("bt_search").is_displayed():
                driver.find_element_by_class_name("bt_search").click()

                # search_btn_id = "bt_search"
                # input_field_name = "query"
                # input_field_el = driver.find_element_by_name(input_field_name)
                # search_btn_el = driver.find_element_by_class_name(search_btn_id)
                # input_field_el.clear()
                # input_field_el.send_keys(query)
                # search_btn_el.click()
        except NoSuchElementException:
            if driver.find_element_by_class_name("bt_search").is_displayed():
                driver.find_element_by_class_name("bt_search").click()

    def strip_tags(self, html):
        regexp = re.compile(r'<[^>]+>')
        return regexp.sub("", html)

    def tear_down(self):
        self.driver.quit()

app = BasicActions()
app.master.title("Auto Bot")
app.master.minsize(400, 200)
app.mainloop()

