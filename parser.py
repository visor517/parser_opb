# импорт библиотек
from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome('chromedriver.exe')

file = open(f'result/theme_A1.csv', 'w', encoding='utf-8') 

# Переход по страницам (билетам)
for number in range(1,17):
    url = f'https://tests24.su/a-1-bilet-{number}-2019/'  
    driver.get(url)

    driver.execute_script('document.querySelectorAll(".watu-question").forEach(function(i) {i.style.display = "block"})') #раскрываем все вопросы
    for question in driver.find_elements_by_css_selector('.question-choices'):
        question.find_element_by_tag_name('input').click()  #отмечаем первые варианты в каждом вопросе

    driver.find_element_by_id('action-button').submit() #отправляем форму
    
    try:    #иногда вылетае алерт, тк вопросы не просматривались. убираем его
        driver.switch_to_alert().accept()
    except Exception:
        print('Алерта нет')

    time.sleep(3) #ждем загрузки страницы с результатом

    requiredHtml = driver.page_source
    soup = BeautifulSoup(requiredHtml, 'lxml')

    # вопрос
    for question_card in soup.find_all('div', class_ = 'show-question'):
        question = question_card.find('div', class_ = 'show-question-content').text
        answers_list = []
        for answer in question_card.find_all('li', class_ = 'answer'):
            answer_text = answer.span.text
            hint = answer.find('span', class_ = 'watupro-screen-reader')
            if hint:
                if hint.text == 'правильно':
                    answer_text = 'true' + answer_text
            answers_list.append(answer_text)
        answers = ';'.join(answers_list)
        file.write(f'{number};"{question}";"{answers}"\n')

file.close()

driver.quit()