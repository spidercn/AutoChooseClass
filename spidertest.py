import time
from configure import Configure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 初始化,可以进行相关的配置
def init(url):
    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    return driver, wait


# 此函数专门用于教务系统的登录与页面跳转的处理
def auto_login(driver, wait):
    cfg = Configure()
    wait.until(EC.presence_of_element_located((By.XPATH,
                                               '/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div/div[2]/div[2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/div[2]/form/div[1]/nz-input-group/input'))).send_keys(
        cfg.username)

    wait.until(EC.presence_of_element_located((By.XPATH,
                                               '/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div/div[2]/div[2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/div[2]/form/div[2]/nz-input-group/input'))).send_keys(
        cfg.password)

    wait.until(EC.presence_of_element_located((By.XPATH,
                                               '/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div/div[2]/div[2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/div[2]/form/div[6]/div/button'))).click()

    # 唯一可能发生问题的地方
    flag = False
    while not flag:
        try:
            driver.refresh()
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[1]'))).click()
            flag = True
        except Exception as e:
            pass

    wait.until(EC.presence_of_element_located((By.XPATH,
                                               '/html/body/div[1]/section/section/main/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[13]/span'))).click()

    # 页面跳转1
    all_handles = driver.window_handles
    new_window_handle = all_handles[1]
    driver.switch_to.window(new_window_handle)

    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[1]/div/ul/li[6]/a'))).click()

    # 页面跳转2
    all_handles = driver.window_handles
    new_window_handle = all_handles[2]
    driver.switch_to.window(new_window_handle)


# 自主选课设计
def choose(driver, wait):
    # 点击查询
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[1]/div/div/div/div/span/button[1]'))).click()

    # 定位选课列表
    cls_list = driver.find_elements(By.XPATH, '//*[@class="body_tr"]')
    # 做一个小小的记录
    total = len(cls_list)
    succ = 0
    fail = 0
    # 主动降速等待页面加载
    time.sleep(1.8)
    for cls in cls_list:
        try:
            cls.find_element(By.XPATH, './/*[@class="an"]').click()
            succ += 1
        except Exception as e:
            print('无法定位元素')
            fail += 1
    return total, succ, fail


if __name__ == '__main__':
    s1 = time.time()
    url = 'https://sso.qlu.edu.cn/login'
    driver, wait = init(url)
    auto_login(driver, wait)
    total, succ, fail = choose(driver, wait)
    s2 = time.time()
    print(f'已全部完成,总的选课数{total},成功选课数{succ},失败选课数{fail}')
    print('总用时:', s2 - s1, '秒')
