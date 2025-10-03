import allure


@allure.feature("Управление заметками")
@allure.story("Создание заметки")
@allure.title("Успешное создание заметки")
def test_CreateNote(http, base_url): 
    body = {
        "title": "Моя первая заметка",
        "content": "Это содержимое моей заметки"
    }
    
    with allure.step("Отправка POST запроса для создания заметки"):
        r = http.post(f"{base_url}/note", json=body, timeout=10) 
    
    with allure.step("Проверка статуса 201 Created"):
        assert r.status_code == 201
    
    with allure.step("Проверка Content-Type"):
        assert "application/json" in r.headers.get("Content-Type", "").lower() 
    
    with allure.step("Проверка тела ответа"):
        data = r.json() 
        print(data)
        assert any("created" in u for u in data) 


@allure.feature("Управление заметками")
@allure.story("Создание заметки")
@allure.title("Создание заметки без заголовка")
def test_CreateNoteNoTitle(http, base_url): 
    body = {
        "content": "Это содержимое моей заметки"
    }
    
    with allure.step("Отправка POST запроса без заголовка"):
        r = http.post(f"{base_url}/note", json=body, timeout=10) 

    with allure.step("Проверка статуса 409 Conflict"):
        assert r.status_code == 409


@allure.feature("Управление заметками")
@allure.story("Создание заметки")
@allure.title("Создание заметки без содержимого")
def test_CreateNoteNoContent(http, base_url): 
    body = {
        "title": "Моя первая заметка"
    }
    
    with allure.step("Отправка POST запроса без содержимого"):
        r = http.post(f"{base_url}/note", json=body, timeout=10) 

    with allure.step("Проверка статуса 409 Conflict"):
        assert r.status_code == 409


@allure.feature("Управление заметками")
@allure.story("Получение всех заметок")
@allure.title("Успешное получение всех заметок")
def test_getAllNotes(http, base_url):
    with allure.step("Отправка GET запроса для получения всех заметок"):
        r = http.get(f"{base_url}/notes", timeout=10) 

    with allure.step("Проверка статуса 200 OK"):
        assert r.status_code == 200
    
    with allure.step("Проверка Content-Type"):
        assert "application/json" in r.headers.get("Content-Type", "").lower()
    
    with allure.step("Проверка структуры ответа"):
        data = r.json() 
        print(data)
        assert isinstance(data, list)  
        assert all(isinstance(u, dict) and "id" in u for u in data)


@allure.feature("Управление заметками")
@allure.story("Получение заметки по ID")
@allure.title("Получение заметки по существующему ID")
def test_getNoteByID(http, base_url):
    id = 1
    with allure.step(f"Отправка GET запроса для заметки с ID={id}"):
        r = http.get(f"{base_url}/note/{id}", timeout=10) 

    with allure.step("Проверка статуса 200 OK"):
        assert r.status_code == 200
    
    with allure.step("Проверка Content-Type"):
        assert "application/json" in r.headers.get("Content-Type", "").lower()
    
    with allure.step("Получение данных ответа"):
        data = r.json() 
        print(data)


@allure.feature("Управление заметками")
@allure.story("Обновление заметки")
@allure.title("Обновление заметки по ID")
def test_putNoteByID(http, base_url): 
    body = {
        "title": "ЗАМЕНА заметки",
        "content": "Это содержимое моей заметки"
    }
    id = 1
    with allure.step(f"Отправка PUT запроса для обновления заметки с ID={id}"):
        r = http.put(f"{base_url}/note/{id}", json=body, timeout=10) 
    
    with allure.step("Проверка статуса 204 No Content"):
        assert r.status_code == 204


@allure.feature("Управление заметками")
@allure.story("Поиск заметки по заголовку")
@allure.title("Поиск заметки по существующему заголовку")
def test_getNoteByTitle(http, base_url):
    title = 'ЗАМЕНА заметки'
    with allure.step(f"Поиск заметки по заголовку: {title}"):
        r = http.get(f"{base_url}/note/read/{title}", timeout=10) 

    with allure.step("Проверка статуса 200 OK"):
        assert r.status_code == 200
    
    with allure.step("Проверка Content-Type"):
        assert "application/json" in r.headers.get("Content-Type", "").lower()
    
    with allure.step("Получение данных ответа"):
        data = r.json() 
        print(data)


@allure.feature("Управление заметками")
@allure.story("Поиск заметки по заголовку")
@allure.title("Поиск заметки по несуществующему заголовку")
def test_getNoteByTitleNoCreate(http, base_url):
    title = 'ТАКОГО ТАЙТЛА НЕТ'
    with allure.step(f"Поиск заметки по несуществующему заголовку: {title}"):
        r = http.get(f"{base_url}/note/read/{title}", timeout=10) 

    with allure.step("Проверка статуса 404 Not Found"):
        assert r.status_code == 404


@allure.feature("Управление заметками")
@allure.story("Обновление заметки")
@allure.title("Обновление заметки без данных")
def test_putNoteByIDnoInfo(http, base_url):   
    body = {}
    id = 1
    with allure.step(f"Отправка PUT запроса без данных для ID={id}"):
        r = http.put(f"{base_url}/note/{id}", timeout=10) 
    
    with allure.step("Проверка статуса 204 No Content"):
        assert r.status_code == 204


@allure.feature("Управление заметками")
@allure.story("Удаление заметки")
@allure.title("Удаление заметки по существующему ID")
def test_deleteNoteByID(http, base_url):
    id = 1
    with allure.step(f"Отправка DELETE запроса для ID={id}"):
        r = http.delete(f"{base_url}/note/{id}", timeout=10) 
    
    with allure.step("Проверка статуса 204 No Content"):
        assert r.status_code == 204

    with allure.step("Проверка что заметка удалена (GET запрос должен вернуть 404)"):
        r = http.get(f"{base_url}/note/{id}", timeout=10)
        data = r.json() 
        assert r.status_code == 404, "Ждём 404 статус"


@allure.feature("Управление заметками")
@allure.story("Удаление заметки")
@allure.title("Удаление заметки по несуществующему ID")
def test_deleteNoteByIDnoCreate(http, base_url):
    id = "-1"
    with allure.step(f"Попытка удаления заметки с несуществующим ID={id}"):
        r = http.delete(f"{base_url}/note/{id}", timeout=10) 
    
    with allure.step("Проверка статуса 409 Conflict"):
        assert r.status_code == 409


@allure.feature("Управление заметками")
@allure.story("Удаление заметки")
@allure.title("Удаление заметки по некорректному ID (строка)")
def test_deleteNoteByIDnoString(http, base_url):
    id = "HAHAHAHA id lol"
    with allure.step(f"Попытка удаления заметки с некорректным ID={id}"):
        r = http.delete(f"{base_url}/note/{id}", timeout=10) 
    
    with allure.step("Проверка статуса 409 Conflict"):
        assert r.status_code == 409


@allure.feature("Управление заметками")
@allure.story("Создание заметки")
@allure.title("Создание заметки без данных")
def test_CreateNoteNoInfo(http, base_url): 
    body = {}
    with allure.step("Попытка создания заметки без данных"):
        r = http.post(f"{base_url}/note", json=body, timeout=10) 

    with allure.step("Проверка статуса 409 Conflict"):
        assert r.status_code == 409