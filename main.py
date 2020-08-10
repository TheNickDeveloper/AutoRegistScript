import os
import json
import pandas as pd
import Models.AccountDetails as ad
import Models.EmaiModel as em
import Services.OutlookHelper as outlook_helper
import Services.WebFormFillingHelper as webfrom_helper
import Services.LogHelper as log_helper
import logging

logger = log_helper.LogHelper().logger
logger.info("----------------Start----------------")

try:
    logger.debug("Load config json file.")
    config_file_path = "config.json"
    with open(config_file_path,encoding="utf-8") as f:
        config = json.load(f)

    logger.debug("Load account details from excel.")
    account_details_file_path = config['account_details_file_path']
    df = pd.read_excel(account_details_file_path)

    account_list = []
    for ind in df.index:
        user_id = df['UserId'][ind]
        user_name = df['UserName'][ind]
        email_address = df['EmailAddress'][ind]
        locate_region = df['LocateRegion'][ind]

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
    os.startfile("outlook")

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

except Exception as e:
    logger.error(f"{e}")
