# Avito_QA_Spring_2026
Решение ТЗ от Авито по QA (UI + API)

<h2>Настройка и возможности тестов</h2>
<div>Предварительная подготовка</div>
<ul>
  <li>Python 3.13</li>
  <li>Allure</li>
  <li>Pytest</li>
  <li>Requests</li>
  <li>PyLint</li>
  <li>Pytest-xdist</li>
  <li>flake8</li>
</ul>
<h2>Установка окружения и запуск</h2>
1. Клонировать репозиторий
2. Создать виртуальное окружение Python 
3. Установить зависимости <code>pip install -r requirements.txt</code>
4. Запустить тесты с нужными вам параметрами: <code>pytest -v -s</code> - это выдаст подробное описание тестов и все print
5. Для параллельных тестов - <code>pytest -v -s -n auto</code>
6. Чтобы создать отчеты, к 4-5 шагам добавьте --alluredir=*Название папки как вы хотите*
7. allure serve *Название папки, куда вы поместили результат*

:)
