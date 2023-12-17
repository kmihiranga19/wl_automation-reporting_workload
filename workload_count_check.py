import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 5)

driver.get("https://worklenz.com/authenticate")
driver.maximize_window()

actions = ActionChains(driver)
members_wise_project_tasks = []
members_tool_tip_details = []


def main():
    login()
    go_to_projects()


def login():
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Email']"))).send_keys(
        "coyonic318@hupoi.com")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Password']"))).send_keys(
        "Test@12345")
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


def go_to_project_workload():
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Workload']"))).click()


def get_member_wise_toolip_tasks_count():
    left_column = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "fixed-left-column")))
    members = left_column.find_elements(By.CLASS_NAME, "single-member")
    for member in members:
        tool_tip_single_m_tasks_count = []
        member_tool_tip_details = {
            "member_name": "",
            "Total_tasks": "",
            "Tasks_without_start_date": "",
            "Tasks_without_end_date": "",
            "Tasks_without_end_date_start_date": ""
        }
        names_div = member.find_element(By.CLASS_NAME, "name-ellipsis")
        member_name = names_div.find_element(By.CLASS_NAME, "ellipsis").text
        member_stats = member.find_element(By.CLASS_NAME, "bar-no-end-date")
        actions.move_to_element(member_stats).perform()
        time.sleep(2)
        tool_tip = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-tooltip-inner")))
        tasks_type = tool_tip.find_elements(By.TAG_NAME, "div")
        for task_type in tasks_type:
            count = task_type.find_elements(By.CSS_SELECTOR, "span")[-1].text
            numbers_only = re.sub(r'[^0-9]', '', count)
            tool_tip_single_m_tasks_count.append(numbers_only)
        member_tool_tip_details["member_name"] = member_name
        member_tool_tip_details["Total_tasks"] = tool_tip_single_m_tasks_count[0]
        member_tool_tip_details["Tasks_without_start_date"] = tool_tip_single_m_tasks_count[1]
        member_tool_tip_details["Tasks_without_end_date"] = tool_tip_single_m_tasks_count[2]
        member_tool_tip_details["Tasks_without_end_date_start_date"] = tool_tip_single_m_tasks_count[3]
        members_tool_tip_details.append(member_tool_tip_details)
        time.sleep(2)

    return


def get_member_wise_tasks_count():
    left_column = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "fixed-left-column")))
    members = left_column.find_elements(By.CLASS_NAME, "single-member")
    for member in members:
        member_task_details = {
            "Member_name": "",
            "Total_tasks": "",
            "Tasks_without_start_date": 0,
            "Tasks_without_end_date": 0,
            "Tasks_without_end_date_start_date": 0

        }
        names_div = member.find_element(By.CLASS_NAME, "name-ellipsis")
        member_name = names_div.find_element(By.CLASS_NAME, "ellipsis").text
        member_task_details["Member_name"] = member_name
        member.click()
        time.sleep(3)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'All Tasks')]"))).click()
        time.sleep(2)
        total_tasks = wait.until(EC.visibility_of_any_elements_located((By.TAG_NAME, "worklenz-wl-task-list-row")))
        member_task_details["Total_tasks"] = + len(total_tasks)
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Tasks without Start date')]"))).click()
        time.sleep(2)
        try:
            without_start_date = driver.find_elements(By.TAG_NAME, "worklenz-wl-task-list-row")
            member_task_details["Tasks_without_start_date"] = + len(without_start_date)

        except NoSuchElementException:
            print("No Tasks without start date")

        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Tasks without End date')]"))).click()
        time.sleep(2)
        try:

            without_end_date = driver.find_elements(By.TAG_NAME, "worklenz-wl-task-list-row")
            member_task_details["Tasks_without_end_date"] = + len(without_end_date)

        except NoSuchElementException:
            print("No Tasks without end date")

        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(),'Tasks without Start & End dates')]"))).click()
        time.sleep(2)

        try:

            without_end_date_start_date = driver.find_elements(By.TAG_NAME, "worklenz-wl-task-list-row")
            member_task_details["Tasks_without_end_date_start_date"] = + len(without_end_date_start_date)

        except NoSuchElementException:
            print("No Tasks without start date end date")

        driver.find_element(By.XPATH,
                            "//div[@class='ant-drawer ant-drawer-right ng-star-inserted ant-drawer-open']//button[@aria-label='Close']").click()
        members_wise_project_tasks.append(member_task_details)
        time.sleep(3)

    return


def workload_main(teams):
    teams[0].click()  # select need team using team index
    time.sleep(2)
    workload_projects()
    go_to_project_workload()
    get_member_wise_tasks_count()
    get_member_wise_toolip_tasks_count()
    print(members_wise_project_tasks)
    print(members_tool_tip_details)


main()
if driver.current_url == "https://worklenz.com/worklenz/projects":
    print("Successfully loaded")
    teams_ = get_teams()
    workload_main(teams_)

else:
    print("Your are not navigate correct page")
