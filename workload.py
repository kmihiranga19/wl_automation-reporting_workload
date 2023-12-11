import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 5)

driver.get("https://uat.worklenz.com/authenticate")
driver.maximize_window()


def main():
    login()
    go_to_projects()


def login():
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Email']"))).send_keys(
        "nehit83711@lanxi8.com")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Password']"))).send_keys(
        "ceyDigital#00")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']"))).click()
    time.sleep(5)


def go_to_projects():
    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//strong[normalize-space()='Projects']"))).click()
    time.sleep(10)


def get_teams():
    switch_team = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "teams-switch")))
    switch_team.click()
    time.sleep(3)
    teams_list = driver.find_elements(By.CLASS_NAME, "team-list-item")
    time.sleep(3)
    return teams_list


def workload_projects():
    t_body = driver.find_element(By.TAG_NAME, "tbody")
    projects = t_body.find_elements(By.TAG_NAME, "tr")
    projects[0].click()  # select need project using index


def show_need_fields():
    fields_toggle = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//button[@class='ant-btn ant-dropdown-trigger columns-toggle']")))
    fields_toggle.click()
    fields = wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "ant-dropdown-menu-item")))
    label_class = fields[4].get_attribute("class")
    priority_class = fields[6].get_attribute("class")
    if "ant-checkbox-wrapper-checked" not in label_class and priority_class:
        fields[4].click()
        fields[6].click()
        fields_toggle.click()
    else:
        fields_toggle.click()


def get_checked_members():
    membersA = []
    member_dropdown = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "members-dropdown")))
    members = member_dropdown.find_elements(By.TAG_NAME, "li")
    for member in members:
        member_class = member.get_attribute("class")
        if "ant-checkbox-wrapper-checked" in member_class:
            user_select = member.find_element(By.CLASS_NAME, "user-select-none")
            div = user_select.find_element(By.TAG_NAME, "div")
            member_name = div.find_element(By.TAG_NAME, "span").text
            membersA.append(member_name)
            time.sleep(1)

            # member_mail = member.find_element(By.TAG_NAME, "small").text
            # membersA.append(member_mail)

    return membersA


def task_list():
    tasks_rows = wait.until(EC.visibility_of_any_elements_located((By.TAG_NAME, "worklenz-task-list-row")))
    filename = "_records11.csv"
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        fields = ['Member', 'Task_name', 'Start_date', 'End_date']
        csvwriter.writerow(fields)
        for task_row in tasks_rows:
            task_name = task_row.find_element(By.CLASS_NAME, "task-name-text").text
            start_date = task_row.find_element(By.TAG_NAME, "worklenz-task-list-start-date")
            start_date_input = start_date.find_element(By.TAG_NAME, "input")
            start_date_value = start_date_input.get_attribute("value")
            end_date = task_row.find_element(By.TAG_NAME, "worklenz-task-list-end-date")
            end_date_input = end_date.find_element(By.TAG_NAME, "input")
            end_date_value = end_date_input.get_attribute("value")
            task_row.find_element(By.TAG_NAME, "worklenz-task-list-members").click()
            members_list = get_checked_members()
            for member in members_list:
                csvwriter.writerow([member, task_name, start_date_value, end_date_value])
            wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='OK']"))).click()
            time.sleep(2)


def workload_main(teams):
    teams[0].click()    # select need team using team index
    time.sleep(2)
    workload_projects()
    show_need_fields()
    task_list()


main()
if driver.current_url == "https://uat.worklenz.com/worklenz/projects":
    teams_ = get_teams()
    workload_main(teams_)

else:
    print("Your are not navigate correct page")
