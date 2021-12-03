# FR_testwork
Testwork for Fabrika

## Как запустить
### Первоначальная установка 
```
cd FR_testwork
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```
Создаём супер-юзера с именем admin и паролем admin.

### Запуск тестов
Тесты следует запускать при работающем сервере.
```
cd DRF-Poll-Test/tests
pytest
```

## Описание API

См. [API.md](API.md)
