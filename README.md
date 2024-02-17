Чтобы запустить проект, нужно ввести следующие команды:
```bash
docker-compose build
docker-compose up -d
```
далее
```bash
docker-compose exec web sh
```
Проводим миграции и прочие мелочи.
```
python manage.py migrate
```
