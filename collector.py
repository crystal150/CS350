import io
import csv
import requests
import datetime
import time
from bs4 import BeautifulSoup

TRAIN_FILE       = "train.csv"
DEFAULT_INTERVAL = 1800
TRAIN_FILE_HEAD  = ["Insult", "Date", "Comment"]

def writeCsv(fname, text, delimiter = ","):

        prev_data = list()
        try:
                file = open(fname, "r")
                reader = csv.reader(file, delimiter = delimiter)
                for row in reader:
                        if (len(row) > 0):
                                prev_data.append(row)
                file.close()
                if (len(prev_data) > 0 and prev_data[0] == TRAIN_FILE_HEAD):
                        prev_data = prev_data[1:]
        
        except FileNotFoundError as e:
                print("train.csv is created.")

        prev_comment = list()
        for t in prev_data:
                prev_comment.append(t[2])

        prev_comment.sort()
        #print(prev_comment)
        duplicated = [False] * len(text)

        for i in range(0, len(text)):
                if (text[i][2] in prev_comment):
                        duplicated[i] = True

        #print(duplicated)
                

        try:
                file = open(fname, "w")
                writer = csv.writer(file, delimiter = delimiter, dialect = "excel")
                writer.writerow(TRAIN_FILE_HEAD)
                writer.writerows(prev_data)
                for i in range(0, len(text)):
                        if (not duplicated[i]):
                                writer.writerow(text[i])
                file.close()
                return 0
        except IOError as e:
                print(str(e))
                return -1

def webCrawl (url, tag = "", tag_attr_type = "", tag_attr_val = ""):
        if (url == None or tag == None or tag_attr_type == None or tag_attr_val == None):
                return []
        page = 1
        source_code = requests.get(url)
        plain_text = source_code.text
        parsed_text = BeautifulSoup(plain_text, "html.parser")
        comment_text = parsed_text.find_all(tag, attrs={tag_attr_type:tag_attr_val})
        
        #comment_date = parsed_text.find_all("a", attrs={"class":"tweet-timestamp js-permalink js-nav js-tooltip"})
        #print(plain_text)
        text_list = list()
        for t in comment_text:
                text_list.append(t.get_text(strip=True))

        #print(type(plain_text))
                
        return text_list

def webCrawlTwitter (url, tag, datetime_start = list(), datetime_end = list()):
        page = 1
        source_code = requests.get(url)
        plain_text = source_code.text
        parsed_text = BeautifulSoup(plain_text, "html.parser")
        comment_text = parsed_text.find_all(tag, attrs={"lang":"en"})
        text_list = list()
        for t in comment_text:
                text_list.append(t.get_text(strip=True))
        return text_list

def webCrawlInsults (url, tag, datetime_start = list(), datetime_end = list()):
        page = 1
        source_code = requests.get(url)
        plain_text = source_code.text
        parsed_text = BeautifulSoup(plain_text, "html.parser")
        comment_text = parsed_text.find_all(tag, attrs={"lang":"en"})
        text_list = list()
        for t in comment_text:
                text_list.append(t.get_text(strip=True))
        return text_list

def evalTexts (text, datetime_str = "", react_pos = list(), react_neg = list(),
               min_react_rate = 0.75, min_react_num = 5, eval_default = False):
        result_list = list()
        for i in range(0, len(text)):
                current_list = list()
                if (i >= len(react_pos) or i >= len(react_neg) or (min_react_rate < 0 and min_react_num < 0)):
                        if (eval_default == 1):
                                current_list.append("1")
                        elif (eval_default == 0):
                                current_list.append("0")
                elif (react_neg[i] / (react_pos[i] + react_neg[i]) >= min_react_rate
                    and react_neg[i] >= min_react_num):
                        current_list.append("1")
                else:
                        current_list.append("0")
                current_list.append(datetime_str)
                current_list.append("\"" + text[i] + "\"")
                result_list.append(current_list)
        return result_list

def setTimeInterval (newInterval):
        t = newInterval

def operate ():
        time_interval = DEFAULT_INTERVAL
        time_prev = time.clock()
        trial_limit = 1
        trial_cur = 0

        config_txt = open("crawler-config.txt", 'r')
        config_lines = list()
        config_pages = list()
        while True:
                line = config_txt.readline()
                config_lines.append(line)
                if not line:
                        break
        for l in config_lines:
                l = l.replace("\n", "")
                l = l.replace(" ", "")
                config_line_variable = ""
                config_line_syntax = True
                config_line_define = l.split("=")

                if (len(config_line_define) != 2):
                        config_line_syntax = False

                if (config_line_syntax == True):
                        config_line_p_str = config_line_define[0].split("[")
                        config_line_p_int = [None] * (len(config_line_p_str) - 1)
                        for i in range (0, len(config_line_p_int)):
                                config_line_p_int[i] = int(config_line_p_str[i + 1][:-1])

                        #print(config_line_p_int)

                        config_line_variable = config_line_p_str[0]
                        #print(config_line_variable)
                        if (config_line_variable == "pages_num"):
                                config_pages_num = int(config_line_define[1])
                                config_pages = [None] * config_pages_num
                                config_tags = [None] * config_pages_num
                                config_tags_at = [None] * config_pages_num
                                config_tags_av = [None] * config_pages_num
                                config_pos_react_tags = [None] * config_pages_num
                                config_pos_react_tags_at = [None] * config_pages_num
                                config_pos_react_tags_av = [None] * config_pages_num
                                config_neg_react_tags = [None] * config_pages_num
                                config_neg_react_tags_at = [None] * config_pages_num
                                config_neg_react_tags_av = [None] * config_pages_num
                                config_eval_neg_rate = [-1] * config_pages_num
                                config_eval_neg_num = [-1] * config_pages_num
                                config_eval_default = [False] * config_pages_num
                                config_exclude_str = [[]] * config_pages_num
                                config_trim_start_str = [[]] * config_pages_num
                                config_trim_end_str = [[]] * config_pages_num
                        if (config_line_variable == "pages"):
                                config_pages[config_line_p_int[0]] = config_line_define[1]
                        if (config_line_variable == "timeinterval"):
                                time_interval = int(config_line_define[1])
                        if (config_line_variable == "trial_limit"):
                                trial_limit = int(config_line_define[1])
                        if (config_line_variable == "tag"):
                                config_tags[config_line_p_int[0]] = config_line_define[1]
                        if (config_line_variable == "tag_attr_type"):
                                config_tags_at[config_line_p_int[0]] = config_line_define[1]
                        if (config_line_variable == "tag_attr_val"):
                                config_tags_av[config_line_p_int[0]] = config_line_define[1]
                        if (config_line_variable == "pos_react_tag"):
                                config_pos_react_tags[config_line_p_int[0]] = config_line_define[1]
                        if (config_line_variable == "pos_react_tag_attr_type"):
                                config_pos_tags_at[config_line_p_int[0]] = config_line_define[1]
                        if (config_line_variable == "pos_react_tag_attr_val"):
                                config_pos_tags_av[config_line_p_int[0]] = config_line_define[1]
                        if (config_line_variable == "neg_react_tag"):
                                config_neg_react_tags[config_line_p_int[0]] = config_line_define[1]
                        if (config_line_variable == "neg_react_tag_attr_type"):
                                config_neg_tags_at[config_line_p_int[0]] = config_line_define[1]
                        if (config_line_variable == "neg_react_tag_attr_val"):
                                config_neg_tags_av[config_line_p_int[0]] = config_line_define[1]
                        if (config_line_variable == "eval_neg_rate"):
                                config_eval_neg_rate[config_line_p_int[0]] = float(config_line_define[1])
                        if (config_line_variable == "eval_neg_rate"):
                                config_eval_neg_num[config_line_p_int[0]] = int(config_line_define[1])
                        if (config_line_variable == "eval_default"):
                                config_eval_default[config_line_p_int[0]] = int(config_line_define[1])
                        if (config_line_variable == "exclude_str"):
                                config_exclude_str[config_line_p_int[0]] = config_line_define[1].split(",")
                                #print (config_exclude_str[config_line_p_int[0]])
                        if (config_line_variable == "trim_start_str"):
                                config_trim_start_str[config_line_p_int[0]] = config_line_define[1].split(",")
                                #print (config_trim_start_str[config_line_p_int[0]])
                        if (config_line_variable == "trim_end_str"):
                                config_trim_end_str[config_line_p_int[0]] = config_line_define[1].split(",")
                                #print (config_trim_end_str[config_line_p_int[0]])
                                
                     
        config_txt.close()

        for i in range (0, len(config_pages)):
                for j in range(0, len(config_exclude_str[i])):
                        config_exclude_str[i][j] = config_exclude_str[i][j].replace("\\n", "\n")
                        config_exclude_str[i][j] = config_exclude_str[i][j].replace("\\t", "\t")
                        config_exclude_str[i][j] = config_exclude_str[i][j].replace("\\b", "\b")
                        config_exclude_str[i][j] = config_exclude_str[i][j].replace("\\\\", "\\")
                for j in range(0, len(config_trim_start_str[i])):
                        config_trim_start_str[i][j] = config_trim_start_str[i][j].replace("\\n", "\n")
                        config_trim_start_str[i][j] = config_trim_start_str[i][j].replace("\\t", "\t")
                        config_trim_start_str[i][j] = config_trim_start_str[i][j].replace("\\b", "\b")
                        config_trim_start_str[i][j] = config_trim_start_str[i][j].replace("\\\\", "\\")
                for j in range(0, len(config_trim_end_str[i])):
                        config_trim_end_str[i][j] = config_trim_end_str[i][j].replace("\\n", "\n")
                        config_trim_end_str[i][j] = config_trim_end_str[i][j].replace("\\t", "\t")
                        config_trim_end_str[i][j] = config_trim_end_str[i][j].replace("\\b", "\b")
                        config_trim_end_str[i][j] = config_trim_end_str[i][j].replace("\\\\", "\\")

        #print ("pages : ")
        #print (config_pages)
        #print ("tags : ")
        #print (config_tags)
        #print ("attr_types : ")
        #print (config_tags_at)
        #print ("attr_vals : ")
        #print (config_tags_av)

        #print(collected_text_result)
        
        while(trial_limit < 0 or trial_cur < trial_limit):

                datetime_now = datetime.datetime.now()
                dt_year = str(datetime_now.year)
                dt_month = str(datetime_now.month)
                if (len(dt_month) < 2):
                        dt_month = "0" + dt_month
                dt_day = str(datetime_now.day)
                if (len(dt_day) < 2):
                        dt_day = "0" + dt_day
                dt_hour = str(datetime_now.hour)
                if (len(dt_hour) < 2):
                        dt_hour = "0" + dt_hour
                dt_min = str(datetime_now.minute)
                if (len(dt_min) < 2):
                        dt_min = "0" + dt_min
                dt_sec = str(datetime_now.second)
                if (len(dt_sec) < 2):
                        dt_sec = "0" + dt_sec

                datetime_str = dt_year + dt_month + dt_day + dt_hour + dt_min + dt_sec + "Z"
                #print (datetime_str)
                evaluated_text_result = list()

                for i in range (0, len(config_pages)):
                        if (config_pages[i] != None and config_tags[i] != None and
                            config_tags_at[i] != None and config_tags_av[i] != None):
                                collected_text = webCrawl(url = config_pages[i], tag = config_tags[i],
                                                          tag_attr_type = config_tags_at[i],
                                                          tag_attr_val = config_tags_av[i])
                                collected_pos_reacts = webCrawl(url = config_pages[i], tag = config_pos_react_tags[i],
                                                                tag_attr_type = config_pos_react_tags_at[i],
                                                                tag_attr_val = config_pos_react_tags_av[i])
                                collected_neg_reacts = webCrawl(url = config_pages[i], tag = config_neg_react_tags[i],
                                                                tag_attr_type = config_neg_react_tags_at[i],
                                                                tag_attr_val = config_neg_react_tags_av[i])
                                for j in range(0, len(collected_text)):
                                                collected_text[j] = collected_text[j].replace("\x92", "\'")

                                for t in collected_text:
                                        for s in config_exclude_str[i]:
                                                collected_text.remove(t)
                                for j in range(0, len(collected_text)):
                                        for s in config_trim_start_str[i]:
                                                collected_text[j] = collected_text[j].split(s)[-1]
                                for j in range(0, len(collected_text)):
                                        for s in config_trim_end_str[i]:
                                                collected_text[j] = collected_text[j].split(s)[0]

                                for t in collected_text:
                                        if (t == ""):
                                                collected_text.remove("")
                                #print(collected_text)

                                evaluated_text = evalTexts (collected_text, datetime_str = datetime_str,
                                                            react_pos = collected_pos_reacts,
                                                            react_neg = collected_neg_reacts,
                                                            min_react_rate = config_eval_neg_rate[i],
                                                            min_react_num = config_eval_neg_num[i],
                                                            eval_default = config_eval_default[i])
                        
                                        
                        evaluated_text_result = evaluated_text_result + evaluated_text

                #print(evaluated_text_result)
                
                #print(datetime_now)
                #collected_text = webCrawl(url = "http://www.gotlines.com/insults/")
                #result_list = evalTexts(collected_text)
                writeCsv(TRAIN_FILE, evaluated_text_result)
                trial_cur = trial_cur + 1
                time_elapsed = 0
                if(trial_limit < 0 or trial_cur < trial_limit):
                        time_prev = time.clock()
                        while(time_elapsed < 10):
                                time_cur = time.clock()
                                time_tick = time_cur - time_prev
                                time_prev = time_cur
                                time_elapsed = time_elapsed + time_tick
                
        time_end = time.clock()

        print ("Crawling Ended")

operate()

