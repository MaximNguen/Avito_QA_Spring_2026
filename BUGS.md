<h1>Баг-репорты API микросервиса у Avito</h1>
<p>Документация обнаруженных дефектов в ходе тестирования</p>
</header>
<h2>Обнаруженные дефекты</h2>

<h3>BUG-001: Неправильный код ответа при получении всех объявлений</h3>

<table>
<tr>
    <th>Поле</th>
    <th>Значение</th>
</tr>
<tr>
    <td><strong>ID бага:</strong></td>
    <td>BUG-001</td>
</tr>
<tr>
    <td><strong>Заголовок:</strong></td>
    <td>Неправильный код ответа при получении всех объявлений</td>
</tr>
<tr>
    <td><strong>Серьезность:</strong></td>
    <td>Высокая</td>
</tr>
<tr>
    <td><strong>Приоритет:</strong></td>
    <td>Высокий</td>
</tr>
<tr>
    <td><strong>Модуль:</strong></td>
    <td>API / Получение объявлений у продавца</td>
</tr>
<tr>
    <td><strong>Окружение:</strong></td>
    <td>Python 3.13, requests, qa-internship.avito.com</td>
</tr>
<tr>
    <td><strong>Статус:</strong></td>
    <td>Открыт</td>
</tr>
<tr>
    <td><strong>Найден в тест-кейсе:</strong></td>
    <td>TC-008, при вводе несуществующего sellerID (Валидный)</td>
</tr>
</table>
<h3>BUG-002: Неправильный код ответа при создании объявления с отрицательной ценой</h3>

<table>
<tr>
    <th>Поле</th>
    <th>Значение</th>
</tr>
<tr>
    <td><strong>ID бага:</strong></td>
    <td>BUG-002</td>
</tr>
<tr>
    <td><strong>Заголовок:</strong></td>
    <td>Неправильный код ответа при создании объявления с отрицательной ценой</td>
</tr>
<tr>
    <td><strong>Серьезность:</strong></td>
    <td>Слабая</td>
</tr>
<tr>
    <td><strong>Приоритет:</strong></td>
    <td>Средняя</td>
</tr>
<tr>
    <td><strong>Модуль:</strong></td>
    <td>API / Создание объявлений</td>
</tr>
<tr>
    <td><strong>Окружение:</strong></td>
    <td>Python 3.13, requests, qa-internship.avito.com</td>
</tr>
<tr>
    <td><strong>Статус:</strong></td>
    <td>Открыт</td>
</tr>
<tr>
    <td><strong>Найден в тест-кейсе:</strong></td>
    <td>TC-003, ожидается 400, но получаем 200</td>
</tr>
</table>