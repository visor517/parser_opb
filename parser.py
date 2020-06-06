# импорт библиотек
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome('chromedriver.exe') #добавить , options=chrome_options для Headless Chrome

# Переход по страницам (билетам)
for number in range(1,17):
    url = f'https://tests24.su/a-1-bilet-{number}-2019/'  
    driver.get(url)

    driver.execute_script('document.querySelectorAll(".watu-question").forEach(function(i) {i.style.display = "block"})') #раскрываем все вопросы
    for question in driver.find_elements_by_css_selector('.question-choices'):
        question.find_element_by_tag_name('input').click()  #отмечаем первые варианты в каждом вопросе

    driver.find_element_by_id('action-button').submit() #отправляем форму
    
    if driver.switch_to_alert():
        driver.switch_to_alert().accept()   #иногда вылезает alert при отправке тк проверяется переход по страницам, а его не было

    time.sleep(2)

    ticket_file = open(f'result/ticket_a1_{number}.txt', 'w', encoding='utf-8')  

    requiredHtml = driver.page_source
    soup = BeautifulSoup(requiredHtml, 'lxml')

    # билет
    ticket = soup.find('h1', class_ = 'entry-title').text
    ticket_file.write(ticket)

    # вопрос
    for question_card in soup.find_all('div', class_ = 'show-question'):
        question_line = []
        question_line.append(question_card.find('div', class_ = 'show-question-content').text)
        for answer in question_card.find_all('li', class_ = 'answer'):
            question_line.append(answer.text.replace('неправильно',''))
                
        ticket_file.write('\n' + ';'.join(question_line))

    ticket_file.close()

driver.quit()