from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of, element_to_be_clickable


class AddressBookAPI:
    def __init__(self):
        self.wd = webdriver.Firefox()
        self.wd.implicitly_wait(5)

    def open_home_page(self):
        wd = self.wd
        # Open home page
        wd.get("http://localhost:8888/addressbook/")

    def login(self, username, password):
        self.open_home_page()
        wd = self.wd
        # Login
        wd.find_element_by_name("user").click()
        wd.find_element_by_name("user").clear()
        wd.find_element_by_name("user").send_keys(username)
        wd.find_element_by_name("pass").click()
        wd.find_element_by_name("pass").clear()
        wd.find_element_by_name("pass").send_keys(password)
        button = wd.find_element_by_xpath("//form[@id='LoginForm']/input[3]")
        button.click()
        WebDriverWait(wd, 15).until(staleness_of(button))

    def is_element_present(self, by, locator):
        wd = self.wd
        try:
            wd.find_element(by, locator)
            return True
        except NoSuchElementException:
            return False

    def is_group_present(self):
        self.open_group_page()
        return self.is_element_present(By.NAME, "selected[]")

    def open_group_page(self):
        wd = self.wd
        # Finding link with waiting when it will be clickable
        group_link = WebDriverWait(wd, 15).until(element_to_be_clickable((By.XPATH, '//*[@id="nav"]/ul/li[3]/a')))
        # group_link = wd.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')
        group_link.click()
        WebDriverWait(wd, 15).until(staleness_of(group_link))

    def create_group(self, group):
        wd = self.wd
        # Init group creation
        wd.find_element_by_name("new").click()
        # Fill group form
        if group.name is not None:
            wd.find_element_by_name("group_name").click()
            wd.find_element_by_name("group_name").clear()
            wd.find_element_by_name("group_name").send_keys(group.name)
        if group.header is not None:
            wd.find_element_by_name("group_header").click()
            wd.find_element_by_name("group_header").clear()
            wd.find_element_by_name("group_header").send_keys(group.header)
        if group.footer is not None:
            wd.find_element_by_name("group_footer").click()
            wd.find_element_by_name("group_footer").clear()
            wd.find_element_by_name("group_footer").send_keys(group.footer)
        # Submit group
        wd.find_element_by_name("submit").click()

    def delete_group_by_number(self, number):
        wd = self.wd
        checkboxes = wd.find_elements_by_name("selected[]")
        checkboxes[number].click()
        wd.find_element_by_name("delete").click()

    def return_to_group_page(self):
        wd = self.wd
        # Return to group page
        link = wd.find_element_by_link_text("group page")
        link.click()
        WebDriverWait(wd, 15).until(staleness_of(link))

    def logout(self):
        wd = self.wd
        # Finding link with waiting when it will be clickable
        link = WebDriverWait(wd, 15).until(element_to_be_clickable((By.CSS_SELECTOR, 'form[name="logout"] > a')))
        link.click()

    def find_message(self):
        wd = self.wd
        return wd.find_element_by_css_selector("div.msgbox").text

    def destroy(self):
        self.wd.quit()
