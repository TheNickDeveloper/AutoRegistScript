from os import startfile
from pandas import read_excel
from json import load
from Services.DataVerifier import DataVerifier
from Services.ExceptionHelper import BlankDataException
import win32api,win32con
import Models.AccountDetails as ad
import Models.EmaiModel as em
import Services.OutlookHelper as outlook_helper
import Services.WebFormFillingHelper as webfrom_helper
import Services.LogHelper as log_helper
import Services.DataVerifier as data_verify_helper
import logging
from datetime import datetime


logger = log_helper.LogHelper().logger
logger.info("----------------Start----------------")

dv_helper = DataVerifier()

try:
    logger.debug("Load config json file.")
    auto_fillinger = None
    config_file_path = r'.\tools\config.json'

    with open(config_file_path,encoding="utf-8") as f:
        config = load(f)

    logger.debug("Load account details from excel.")
    account_details_file_path = config['account_details_file_path']
    df = read_excel(account_details_file_path, sheet_name="申请表格", skiprows=[0,2,3])

    account_list = []
    for ind in df.index:
        user_id = dv_helper.is_null(df['工号'][ind],'工号')
        user_name = dv_helper.is_null(df['姓名'][ind],'姓名')
        email_address = dv_helper.is_null(df['邮箱地址'][ind],'邮箱地址')
        locate_region = dv_helper.is_null(df['人员所在地（填写城市）'][ind],'人员所在地（填写城市）')

        person_account_details = ad.AccountDetails(user_id, user_name, email_address, locate_region)
        account_list.append(person_account_details)

    username = config['username']
    password  = config['password']
    cot_url = config['url_options']["cot_url"]
    cot_emp_url = config['url_options']["cot_emp_url"]
    cot_user_url = config['url_options']["cot_user_url"]

    auto_fillinger = webfrom_helper.WebFormFillingHelper( username, password, cot_url, cot_emp_url, cot_user_url, logger)
    auto_fillinger.login_cot_webpage()

    # open another outlook in case user did not open it
    startfile("outlook")

    # iterate account infor for filling
    for account in account_list:
        logger.info(f"Start creating account for user {account.user_name}")
        is_account_created = auto_fillinger.regist_ppl_info(account)

        if is_account_created:
            logger.info(f"Account creating completed. Send email to inform user.")
            new_mail = em.Email(account)
            outlook = outlook_helper.OutlookHelper(new_mail)
            outlook.send_mail()

    logger.info("Finish.")
    win32api.MessageBox(0, "Process completed!", "COT account create",win32con.MB_OK)


except BlankDataException as e:
    win32api.MessageBox(0, f"{e}", "Error",win32con.MB_OK)
    logger.info(e)
    logger.exception(e)

    logger.exception("nono")


except Exception as e:
    win32api.MessageBox(0, f"{e}", "Error",win32con.MB_OK)
    logger.info(e)

    # logger has some problem
    logger.exception(e)
    logger.exception("nono")



finally:
    if auto_fillinger is not None:
        auto_fillinger.dispose_driver()
    logger.info("finish")
    
