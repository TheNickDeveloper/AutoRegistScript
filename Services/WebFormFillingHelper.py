from sys import path
from os import getcwd

path.append(getcwd())

from Models.AccountDetails import AccountDetails
from Services.LogHelper import LogHelper
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class  WebFormFillingHelper():
    def __init__(self, username, password, target_url, base_emp_url, base_user_url, logger: LogHelper):
        chromeDriverPath = r'.\tools\chromedriver.exe'
        self.__driver = webdriver.Chrome(chromeDriverPath)
        self.__target_url = target_url
        self.__baseEmp_url = base_emp_url
        self.__baseUser_url = base_user_url
        self.__username = username
        self.__password = password
        self.__logger = logger


    def login_cot_webpage(self):
        self.__logger.debug("Navigate to COT website")
        self.__driver.get(self.__target_url)
        self.__driver.find_element_by_id("userAccount").send_keys(self.__username)
        self.__driver.find_element_by_name("userPassword").send_keys(self.__password,'\ue007')


    def regist_ppl_info(self, account_details:AccountDetails):
        user_id = account_details.user_id
        user_name = account_details.user_name
        password = "1111"
        region = account_details.region

        if not self.__is_emp_id_exsit(user_id):
            self.__create_emp_account(user_id, user_name, region)
        
        if not self.__is_user_id_exsit(user_id):
            self.__create_user_account(user_id, password)
            return True
        else:
            self.__logger.warning(f"{user_id} has already exsited.")
            return False

    
    def __is_emp_id_exsit(self, user_id):
        self.__logger.debug(f"Check if people id exsit in emp management.")
        self.__driver.get(self.__baseEmp_url)
        self.__driver.refresh()
        self.__driver.switch_to_frame("main")
        self.__driver.find_element_by_name("$lk_empCode").send_keys(user_id)
        self.__driver.find_element_by_id("query_A").click()
        data_table = WebDriverWait(self.__driver, 10).until(lambda d: d.find_element_by_class_name("tableBody"))
        emp_id_search_result = data_table.find_elements_by_tag_name("tr")
        return len(emp_id_search_result) > 0
    

    def __is_user_id_exsit(self, user_id):
        self.__logger.debug(f"Check if people id exsit in user management.")
        self.__driver.get(self.__baseUser_url)
        self.__driver.refresh()
        self.__driver.switch_to_frame("main")
        self.__driver.find_element_by_name("$lk_baseEmployee_empCode").send_keys(user_id)
        self.__driver.find_element_by_id("query_A").click()
        data_table = WebDriverWait(self.__driver, 10).until(lambda d: d.find_element_by_class_name("tableBody"))
        emp_id_search_result = data_table.find_elements_by_tag_name("tr")
        return len(emp_id_search_result) > 0
    

    def __create_emp_account(self, user_id, user_name, region):
        self.__logger.debug(f"Navigate to employee account and add memeber.")
        self.__driver.find_element_by_link_text('新增').click()
        self.__driver.find_element_by_name("empCode").send_keys(user_id)
        self.__driver.find_element_by_name("empName").send_keys(user_name)
        self.__driver.find_element_by_name("isEmployee").click()

        self.__logger.debug(f"Radio button click.")
        self.__driver.find_element_by_xpath('//*[@id="SollAuto"]/div/table/tbody/tr[4]/td[2]/input[2]').click()
        self.__driver.find_element_by_xpath('//*[@id="SollAuto"]/div/table/tbody/tr[3]/td[4]/select/option[2]').click()

        self.__logger.debug(f"Region select via pop window.")
        self.__driver.find_element_by_name("geoName").click()
        self.__driver.switch_to_frame("modalDialog")
        search_bar= WebDriverWait(self.__driver, 10).until(lambda d: d.find_element_by_xpath('//*[@id="keyWord"]'))
        search_bar.send_keys(region)
        self.__driver.find_element_by_xpath('//*[@id="keyWordBnt"]').click()
        self.__driver.find_element_by_xpath('//*[@id="buttonBox"]/span[2]').click()
        self.__save_input_ppl_info()

    
    def __create_user_account(self, user_id, password):
        self.__logger.debug(f"Navigate to user account and add memeber.")
        self.__driver.refresh()
        self.__driver.switch_to_frame("main")
        self.__driver.find_element_by_link_text('新增').click()
        self.__driver.find_element_by_name('userAccount').send_keys(user_id)
        self.__driver.find_element_by_name('userPassword').send_keys(password)
        self.__driver.find_element_by_xpath('//*[@id="userScrollAuto"]/table/tbody/tr/td[2]/div/div/table/tbody/tr[1]/td[4]/select/option[2]').click()
        self.__driver.find_element_by_name('empName').click()

        self.__logger.debug(f"Cehck user name from pop up window.")
        self.__driver.switch_to_frame("modalDialog")
        frime_tree = WebDriverWait(self.__driver, 10).until(lambda d: d.find_element_by_xpath('/html/body/iframe'))
        self.__driver.switch_to_frame(frime_tree)
        id_search_bar= WebDriverWait(self.__driver, 10).until(lambda d: d.find_element_by_name('empCode'))
        id_search_bar.send_keys(user_id)
        self.__driver.find_element_by_id("query_A").click()
        first_option= WebDriverWait(self.__driver, 10).until(lambda d: d.find_element_by_xpath('//*[@id="rdo1"]'))
        first_option.click()
        self.__driver.find_element_by_link_text('确定').click()

        self.__logger.debug(f"Check one option from left tree.")
        self.__driver.switch_to_default_content()
        self.__driver.switch_to_frame("main")
        left_frime = WebDriverWait(self.__driver, 10).until(lambda d: d.find_element_by_xpath('//*[@id="leftmenu1"]/iframe'))
        self.__driver.switch_to_frame(left_frime)
        user_right = self.__driver.find_element_by_xpath('//*[@id="t-36036"]/span/i')
        user_right.click()
        self.__save_input_ppl_info()
    

    def __save_input_ppl_info(self):
        self.__logger.debug(f"Save people infor.")
        self.__driver.switch_to_default_content()
        self.__driver.switch_to_frame("main")
        self.__driver.find_element_by_link_text('保存').click()
        

