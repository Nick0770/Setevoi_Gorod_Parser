from selenium import webdriver
from time import sleep
from fake_useragent import FakeUserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from os.path import isfile
from dotenv import load_dotenv
from os import getenv

#  для получения переменных сред
load_dotenv()

#  создаём фейковый user-agent и добавляем его в опции
a = FakeUserAgent().random
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={a}')

#  путь для загрузки файлов
path = getenv('path_to_download')
prefs = {
    "download.default_directory": path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option('prefs', prefs)

#  браузер
url = 'https://netschool.edu22.info/'
driver = webdriver.Chrome(options=options)
action = ActionChains(driver)

#  путь к файлу для дз и оценок
school = getenv('path_to_save')

#  очищение school
with open(school, 'w', encoding='utf-8') as file:
    file.write('')


#  функция парсинга дз
def homework_parsing(side_path, table_path):
    side = driver.find_element(By.XPATH, side_path)
    tables = side.find_elements(By.XPATH, table_path)
    with open(school, 'a', encoding='utf-8') as file:
        for table in tables:
            trs = table.find_elements(By.TAG_NAME, 'tr')
            for tr in trs:
                tds = tr.find_elements(By.TAG_NAME, 'td')
                for td in tds:
                    file.write(td.text + '\n')
                    print(td.text)
    sleep(1)


#  функция для загрузки файлов с дз
def loading_files(col_num, table_num, index=''):
    m = 1
    for _ in range(8):
        try:
            driver.find_element(
                By.XPATH, f'/html/body/div{index}/div[2]/div[1]/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[{col_num}]/div[{table_num}]/diary-day/div/div/table[2]/tbody/tr[{m}]/td[3]/div[2]/assign-attachments/div/i').click()
            sleep(5)
            file_name = driver.find_element(By.CSS_SELECTOR, 'div.name_file.ng-binding').text
            if not isfile(f'{path}\\{file_name}'):
                sleep(1)
                driver.find_element(
                    By.CSS_SELECTOR, 'a.mdi.mdi-file.ng-scope').click()
                sleep(10)
        except:
            pass
        m += 1
    sleep(3)


#  сегодняшний день недели
week_today = datetime.today().strftime('%A')


def main():
    #  основной блок
    try:
        #  открываем сайт
        driver.get(url=url)
        driver.maximize_window()
        sleep(1)

        #  нажимаем на красненькую
        driver.find_element(By.CSS_SELECTOR, '.btn.red').click()
        sleep(1)

        #  выбираем организацию
        driver.find_element(By.CSS_SELECTOR, '.select2-selection.select2-selection--single').click()
        sleep(1)

        driver.find_element(By.CLASS_NAME, 'select2-search__field').send_keys(getenv('organization'))
        sleep(1)

        driver.find_element(By.CLASS_NAME, 'org-name-data').click()
        sleep(1)

        #  вводим логин
        driver.find_element(By.NAME, 'loginname').send_keys(getenv('login'))
        sleep(1)

        #  вводим пароль
        driver.find_element(By.NAME, 'password').send_keys(getenv('password'))
        sleep(1)

        #  вход
        driver.find_element(By.CLASS_NAME, 'primary-button').click()
        sleep(3)
        
        #  в случае, если вход уже был сегодня
        try:
            driver.find_element(By.CLASS_NAME, 'icon-signout').click()
        except:
            pass
        sleep(3)

        #  заходим в отчёты
        driver.find_element(By.CSS_SELECTOR, '.nav.navbar-nav').find_elements(By.TAG_NAME, 'a')[6].click()
        sleep(3)

        #  выбираем зайти в отчёты со всеми оценками
        driver.find_elements(By.CLASS_NAME, 'ng-binding')[7].click()
        sleep(3)

        #  сформировать
        driver.find_element(By.CSS_SELECTOR, '.btn-default').click()
        sleep(3)

        #  получаем инфу с отчёта
        table = driver.find_element(By.CLASS_NAME, 'table-print').find_elements(By.TAG_NAME, 'tr')
        n = 0
        grades = ''
        with open(school, 'a', encoding='utf-8') as file:
            for i in table[2:]:
                tds = i.find_elements(By.TAG_NAME, 'td')
                for td in tds[1:]:
                    grades += td.text + ' '
                grades_to_print = f"{driver.find_elements(By.CLASS_NAME, 'cell-text')[0 + n].text}: {grades}"
                file.write(grades_to_print + '\n')
                print(grades_to_print)
                grades = ''
                n += 1
            file.write('\n')
        print()
        sleep(5)

        #  заходим в дневник
        mouse = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[4]/nav/ul/li[4]/a')
        action.move_to_element(mouse).perform()
        driver.find_element(By.XPATH, '/html/body/div/div[1]/div[4]/nav/ul/li[4]/ul/li[1]/a').click()
        sleep(3)

        #  если сегодня суббота перелистываем
        if week_today == 'Saturday':
            driver.find_element(By.CLASS_NAME, 'button_next').click()
        sleep(2)

        #  парсим дз
        left_change = 0
        right_change = 0
        for _ in range(3):
            left_change += 1
            homework_parsing('/html/body/div/div[2]/div[1]/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[2]',
                             f'/html/body/div/div[2]/div[1]/    div/div/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div[{left_change}]/diary-day/div/div/table[2]/tbody')
        for _ in range(2):
            right_change += 1
            homework_parsing('/html/body/div/div[2]/div[1]/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[3]',
                             f'/html/body/div/div[2]/div[1]/    div/div/div/div[2]/div/div[3]/div/div/div[2]/div[3]/div[{right_change}]/diary-day/div/div/table[2]/tbody')

        #  скачиваем файлы
        #  понедельник, четверг
        loading_files(2, 1)
        loading_files(3, 1)

        #  вторник среда пятница
        loading_files(2, 2, [1])
        loading_files(2, 3, [1])
        loading_files(3, 2, [1])

    except Exception as ex:
        #  вывод ошибок 
        print(ex)
    finally:
        #  закрытие сайта
        driver.find_elements(By.CLASS_NAME, 'hidden-scr-sm')[4].click()
        sleep(3)
        driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary').click()
        sleep(3)
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()
