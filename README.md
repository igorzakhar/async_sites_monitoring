# Утилита для мониторинга сайтов

Данная утилита может использоваться для мониторинга доступности сайтов и отслеживания наступления даты, до которой оплачено доменое имя.

# Установка

Для запуска программы требуется установленный Python 3.5.  
В программе используются следующие сторонние библиотеки:  
- [aiohttp](https://aiohttp.readthedocs.io/en/stable/)
- [aiofiles](https://github.com/Tinche/aiofiles)
- [ph4-python-whois](https://github.com/ph4r05/python-whois)

Используйте команду pip для установки сторонних библиотек из файла зависимостей (или pip3 если есть конфликт с предустановленным Python 2):
```
pip install -r requirements.txt # В качестве альтернативы используйте pip3
```
Рекомендуется устанавливать зависимости в виртуальном окружении, используя [virtualenv](https://github.com/pypa/virtualenv), [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) или [venv](https://docs.python.org/3/library/venv.html).

Так же в программе используется утилита ```whois``` для OC linux.  
Установка утилиты для дистрибутивов linux в кторых используется пакетный менеджер ```apt```:  
```
$ sudo apt-get install whois
```

Для дистрибутивов linux в кторых используется пакетный менеджер ```yum```:  
```
$ yum install jwhois
```
# Запуск программы
Для работы программы требуется текстовый файл, который содержит список сайтов для мониторинга вида:
```
http://domen.org
http://example.ru
https://domen.example.tld
...
```
Для указания файла используется аргумент командной строки ```-f <filename>``` или ```--file <filename>```.

### Пример запуска и вывод результатов:
```
$ python check_sites_health.py -f urls.txt
http://edutula.ru   : status code: 200, days until expiry: 194 days (2018-07-27)
http://schoolmit.ru : status code: 200, days until expiry: 96 days (2018-04-20)
http://socobraz.ru  : status code: 200, days until expiry: 157 days (2018-06-20)
https://github.com  : status code: 200, days until expiry: 999 days (2020-10-09)
https://yandex.ru   : status code: 200, days until expiry: 259 days (2018-09-30)
http://langbridge.ru: status code: 200, days until expiry: 234 days (2018-09-06)
```
