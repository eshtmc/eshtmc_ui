#!/usr/bin/env python

from bs4 import BeautifulSoup
import json
import os
from .config import Config
from .git_eshtmc import Eshtmc

class Agenda:
    def __init__(self, config):
        self.config = config
        self.md_type_data = {
            "date": self.config.MEETING_DATE,
            "count": self.config.MEETING_COUNT,
            "theme": self.config.MEETING_THEME,
            "attendance": {
                "name": self.config.AttendanceName
            },
            "best_awards": {
                "BTTS": self.config.BestTableTopicSpeech,
                "BPS": self.config.BestPreparedSpeech,
                "BE": self.config.BestEvaluator
            },
            "role_takers": self.config.ROLE_TAKERS,
            "speakers": {
                "TT": self.config.TableTopic,
                "perpared_speackers": self.config.PREPARED_SPEAKERS,
            }
        }

    def save_json(self):
        print(json.dumps(self.md_type_data, indent=4))

    def save_speakers(self):
        """"
 ### 103, Balance (2018-08-10)
`TT`  Eve Zhang, Jenny Yu, Jun Liu, Dongchen Tang
`CC7` Siyuan Jia -  kubernetes say hello
`P2` Elvis Jiang - Be like a man
        """
        if not self.is_need_to_update(os.path.join(
                self.config.md_path_dir, "speakers.md")):
            return
        add_content = "### {0}, {1} ({2})   \n`TT` {3}  \n".format(self.md_type_data["count"], self.md_type_data["theme"],
                                                             self.md_type_data["date"],
                                                             self.md_type_data["speakers"]["TT"])

        for i in range(len(self.md_type_data["speakers"]["perpared_speackers"])):
            if self.md_type_data["speakers"]["perpared_speackers"][i]["project_rank"].strip() != "":
                add_content = add_content + "`{0}` {1}-{2}   \n".format(self.md_type_data["speakers"]["perpared_speackers"][i]["project_rank"].strip(),
                                                                     self.md_type_data["speakers"]["perpared_speackers"][i]["people_name"],
                                                                     self.md_type_data["speakers"]["perpared_speackers"][i]["project_name"])
        print(add_content)
        with open(os.path.join(self.config.md_path_dir, "speakers.md"), "a+") as f:
            f.writelines("\n" + add_content)

    def transform_str(self, key):

        return {
            "BTTS": "`Best Table Topic Speech`",
            "BPS": "`Best Prepared Speech`",
            "BE": "`Best Evaluator`"
        }.get(key)

    def save_best_awards(self):
        """"
 ### 101, Self-discipline (2018-07-13)
`Best Table Topic Speech` Nrapendra singh
`Best Prepared Speech` Sarah Zhang
`Best Evaluator` Jony
        """
        if not self.is_need_to_update(os.path.join(
                self.config.md_path_dir, "best-awards.md")):
            return
        add_content = "### {0}, {1} ({2})   \n".format(
            self.md_type_data["count"],
            self.md_type_data["theme"],
            self.md_type_data["date"])
        for key, value in self.md_type_data["best_awards"].items():
            if value != "":
                add_content = add_content + "{0} {1}    \n".format(
                    self.transform_str(key), value)

        print(add_content)
        with open(os.path.join(
                self.config.md_path_dir, "best-awards.md"), "a+") as f:
            f.writelines("\n" + add_content)


    def save_role_takers(self):
        """
### 102, Music (2018-07-27)
`TMD` Michelle Jin
`TTM` Dongchen Tang
`GE` Sarah Zhang
`IE` Jun Liu, Taowen Zhang
`Grammarian` Xin Feng
`Timer` Wujie Zhang
`Ah-Counter` Nrapendra Singh
        """
        if not self.is_need_to_update(os.path.join(
                self.config.md_path_dir, "role-takers.md")):
            return
        add_content = "### {0}, {1} ({2})   \n".format(
            self.md_type_data["count"],
            self.md_type_data["theme"],
            self.md_type_data["date"])
        for key, value in self.md_type_data["role_takers"].items():
            if value != "":
                add_content = add_content + "`{0}` {1}   \n".format(key, value)

        print(add_content)
        with open(os.path.join(
                self.config.md_path_dir, "role-takers.md"), "a+") as f:
            f.writelines("\n" + add_content)

    def save_attendance(self):
        soup = BeautifulSoup(open(os.path.join(
            self.config.md_path_dir, "attendance.html")), "html.parser")
        temp_n = len(soup.find_all('tr'))    # row
        temp_head = []                       # data_time
        name = []
        data = [[] for i in range(temp_n - 1)]
        for i, child_tr in enumerate(soup.find_all('tr')):
            for j, child_th in enumerate(child_tr.find_all('th')):
                if i == 0:
                    temp_head.append(child_th.string)
                else:
                    data[i-1].append(child_th.string)
                    if j == 0:
                        name.append(child_th.string)
        for i in data:
            sum = 0
            for j in i[1:]:
                if j != 0:
                    sum += int(j)
            # print(i[0:1], sum, i)
            # print("test~")

        #  TODO up date the temp_head and data
        if self.md_type_data["date"] not in temp_head and temp_head != []:
            # new record
            temp_head.append(self.md_type_data["date"])
            data[temp_n - 2].append(0)
            print(temp_head)
            print(00, self.md_type_data["attendance"]["name"].split(","))
            temp_attendance_name_list = list(
                set(x.strip() for x in
                    self.md_type_data["attendance"]["name"].split(",")))
        # remove blank,
            print(temp_attendance_name_list)
            print(11, data[:temp_n-1])
            for k, value in enumerate(data[:temp_n-2]):
                # print(k, value)
                if value[0] in temp_attendance_name_list:
                    data[k].append(1)
                    data[temp_n-2][len(temp_head)-1] += 1
                    # total + 1
                    temp_attendance_name_list.remove(value[0])
                    print("remove", value[0], temp_attendance_name_list)
                else:
                    data[k].append(0)

            print(data[:temp_n - 1])
            for i, a_name in enumerate(temp_attendance_name_list):
                if a_name != "":
                    print(i, a_name)
                    temp_list = list()
                    temp_list.append(str(a_name))
                    for j in range(len(temp_head)-2):
                        # don't need to include "name" and "1"
                        temp_list.append(0)
                        pass
                    temp_list.append(1)
                    # flag 1 , meaning the attended
                    data[len(data)-1][len(temp_head) - 1] += 1
                    # total + 1
                    data.insert(temp_n-2+i, temp_list)
        else:
            # update the record
            pass
            # Avoid unnecessary changes not supported it

        html_content = """<h1>Attendance</h1>
<table class="table table-condensed table-bordered">
"""
        for i in range(len(data) + 1):
            html_content += "<tr>"
            if i == 0:
                content = temp_head
            else:
                content = data[i-1]
            for j, value in enumerate(content):
                html_content += "<th>{0}</th>".format(value)
            html_content += "</tr>\n"
        html_content += "</table>\n"
        # print(self.config.HTML_ATTENDANCE_head+html_content+self.config.HTML_ATTENDANCE_end)
        with open(os.path.join(self.config.md_path_dir, "attendance.html"), "w") as f:
            f.writelines(self.config.HTML_ATTENDANCE_head +
                         html_content + self.config.HTML_ATTENDANCE_end)
            print("write....")

    def create_new_record(self):
        print(os.path.exists(self.config.md_path_dir))
        if not os.path.exists(self.config.md_path_dir):
            os.makedirs(self.config.md_path_dir)
            with open("eshtmc.github.io/index.md", "a+") as f:
                f.writelines("\n" + self.config.INDEX_ADD)
        temp = "#### [Home](https://eshtmc.github.io/)    \n"
        if not os.path.exists(os.path.join(
                self.config.md_path_dir, "attendance.html")):
            with open(os.path.join(
                    self.config.md_path_dir, "attendance.html"), "w") as f:
                f.writelines(
                    self.config.HTML_ATTENDANCE_head +
                    self.config.New_Table + self.config.HTML_ATTENDANCE_end)
        if not os.path.exists(os.path.join(
                self.config.md_path_dir, "best-awards.md")):
            with open(os.path.join(
                    self.config.md_path_dir, "best-awards.md"), "w") as f:
                f.writelines(temp)
        if not os.path.exists(os.path.join(
                self.config.md_path_dir, "role-takers.md")):
            with open(os.path.join(
                    self.config.md_path_dir, "role-takers.md"), "w") as f:
                f.writelines(temp)
        if not os.path.exists(os.path.join(
                self.config.md_path_dir, "speakers.md")):
            with open(os.path.join(
                    self.config.md_path_dir, "speakers.md"), "w") as f:
                f.writelines(temp)

    def is_need_to_update(self, filepath):
        with open(filepath, "r") as f:
            content = f.read()
            if content.find(self.config.MEETING_DATE) != -1:
                print("no need to update {0}".format(filepath))
                return False
            else:
                print("updating {0}".format(filepath))
                return True


def github_page(config_dict):
    print(config_dict)

    Config.MEETING_COUNT = config_dict.get("count")
    Config.MEETING_DATE = config_dict.get("date")
    Config.MEETING_THEME = config_dict.get("theme")
    Config.AttendanceName = config_dict.get("attendance")
    Config.TableTopic = config_dict.get("table_topic_speaker")
    Config.BestEvaluator = config_dict.get("best_evaluator_speaker")
    Config.BestPreparedSpeech = config_dict.get("best_prepared_speaker")
    Config.BestTableTopicSpeech = config_dict.get(
        "best_table_topic_speaker")
    Config.PREPARED_SPEAKERS = config_dict.get("prepared_speakers")
    Config.ROLE_TAKERS = {
        "TMD": config_dict.get("toastmaster_of_day"),
        "TTM": config_dict.get("table_topic_master"),
        "GE": config_dict.get("general_evaluator"),
        "IE": config_dict.get("individual_evaluator"),
        "Grammarian": config_dict.get("grammarian"),
        "Timer": config_dict.get("timer"),
        "Ah-counter": config_dict.get("ah_counter")
    }

    #  change the  NEW_DIR_TIMR = "2018.10-2019.03"
    # 2018.04-2018.09
    # 2018.10-2019.03
    # 2019.04-2019.09
    yy, mm, dd = tuple(config_dict.get("date").split("."))
    if 4 <= int(mm) <= 9:
        Config.NEW_DIR_TERM = "{0}.10-{1}.03".format(yy, yy)
    else:
        # (10 <= int(mm) <= 12) or (1 <= int(mm) <= 3)
        Config.NEW_DIR_TERM = "{0}.10-{1}.03".format(yy, str(int(yy) + 1))

    Config.md_path_dir = "eshtmc.github.io/education/meetings/{0}/".format(
        Config.NEW_DIR_TERM)

    Config.INDEX_ADD = """
### {0}
[attendance](https://eshtmc.github.io/education/meetings/{0}/attendance.html)
[best-awards](https://eshtmc.github.io/education/meetings/{0}/best-awards)
[role-takers](https://eshtmc.github.io/education/meetings/{0}/role-takers)
[speakers](https://eshtmc.github.io/education/meetings/{0}/speakers)
        """.format(Config.NEW_DIR_TERM)
    Config.Message = "update {0} #{1} {2}".format(
        Config.MEETING_DATE, Config.MEETING_COUNT, Config.MEETING_THEME)

    tm = Eshtmc(Config)
    ag = Agenda(Config)

    tm.git_clone()

    ag.create_new_record()
    ag.save_json()
    ag.save_speakers()
    ag.save_best_awards()
    ag.save_role_takers()
    ag.save_attendance()

    tm.git_add()
    tm.git_commit()
    tm.git_push()
