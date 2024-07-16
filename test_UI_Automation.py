import pytest
import json
import os
import time
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def log_test_case(test_cases, test_case, test_scenario, input_data, expected_result, actual_result, status):
    log_entry = {
        "Test case": test_case,
        "Test scenario": test_scenario,
        "Input": input_data,
        "Expected result": expected_result,
        "Actual result": actual_result,
        "Status": status
    }
    test_cases.append(log_entry)
    with open("report_pretty.json", "w") as file:
        json.dump(test_cases, file, indent=4)

def generate_report(test_cases):
    table_headers = ["Test case", "Test scenario", "Input", "Expected result", "Actual result", "Status"]
    table_data = [[entry.get(header, "") for header in table_headers] for entry in test_cases]
    with open("report_pretty.json", "a") as file:
        file.write("\n\n")
        file.write(tabulate(table_data, headers=table_headers, tablefmt="grid"))
        file.write("\n\n")

@pytest.fixture(scope="module")
def driver_setup():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def test_cases():
    if os.path.exists("report_pretty.json"):
        os.remove("report_pretty.json")
    return []

class TestUI:

    @pytest.mark.create_board
    def test_create_board(self, driver_setup, test_cases):
        driver = driver_setup
        driver.get("http://localhost:3000/")
        time.sleep(10)

        # Click on the Create new board button
        create_board_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "create-board.hover\\:bg-gray7"))
        )
        create_board_button.click()
        time.sleep(2)

        # Add board title
        board_title_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "new-board-input"))
        )
        board_title_input.send_keys("Test")

        # Click on Create board button
        create_board_submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-cy='new-board-create']"))
        )
        create_board_submit_button.click()
        time.sleep(2)

        actual_result = "Board created successfully" if "Test" in driver.page_source else "Board not created successfully"
        expected_result = "Board created successfully"
        status = "Passed" if actual_result == expected_result else "Failed"

        log_test_case(
            test_cases,
            test_case="Create Board Test",
            test_scenario="Create Board",
            input_data="Test",
            expected_result=expected_result,
            actual_result=actual_result,
            status=status
        )

        assert status == "Passed", f"Test Failed: {actual_result}"
        generate_report(test_cases)

    @pytest.mark.add_list
    def test_add_list(self, driver_setup, test_cases):
        driver = driver_setup

        # first list
        list_title_input01 = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-cy='add-list-input']"))
        )
        list_title_input01.send_keys("test_01")

        # Click on the Add list button for the first list
        add_list_button01 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "button.inline-block.py-1.px-3.mt-1.h-8.text-sm.font-normal.text-center.text-white.bg-green7"))
        )
        add_list_button01.click()
        time.sleep(2)

        # second list
        list_title_input02 = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-cy='add-list-input']"))
        )
        list_title_input02.send_keys("test_02")

        # Click on the Add list button for the second list
        add_list_button02 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "button.inline-block.py-1.px-3.mt-1.h-8.text-sm.font-normal.text-center.text-white.bg-green7"))
        )
        add_list_button02.click()
        time.sleep(2)

        actual_result = "Lists created successfully" if "Add another card" in driver.page_source else "Lists not created successfully"
        expected_result = "Lists created successfully"
        status = "Passed" if actual_result == expected_result else "Failed"

        log_test_case(
            test_cases,
            test_case="Add List Test",
            test_scenario="Add two lists",
            input_data="test_01 and test_02",
            expected_result=expected_result,
            actual_result=actual_result,
            status=status
        )

        assert status == "Passed", f"Test Failed: {actual_result}"
        generate_report(test_cases)

    @pytest.mark.delete_list_action
    def test_delete_list(self, driver_setup, test_cases):
        driver = driver_setup

        # delete_list_select
        delete_list = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-cy='list-options']"))
        )
        delete_list.click()
        time.sleep(2)

        # delete list
        delete_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-cy='delete-list']"))
        )
        delete_button.click()
        time.sleep(2)

        actual_result = "List deleted successfully" if "test_02" not in driver.page_source else "List not deleted successfully"
        expected_result = "List deleted successfully"
        status = "Passed" if actual_result == expected_result else "Failed"

        log_test_case(
            test_cases,
            test_case="Delete List Test",
            test_scenario="Delete a list",
            input_data="Click on delete",
            expected_result=expected_result,
            actual_result=actual_result,
            status=status
        )

        assert status == "Passed", f"Test Failed: {actual_result}"
        generate_report(test_cases)

if __name__ == "__main__":
    pytest.main(["-v"])
