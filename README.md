# Тестовое задание от «ООО СМАРТС-Кванттелеком»
## Должность: Python Backend Developer (Middle)

Необходимо реализовать "удаленный калькулятор". Калькулятор состоит из двух частей - клиентской и серверной (обе без ui, в консоли). Логика работы/использования следующая:
1.	Запускается сервер и клиент (вручную, запуском .py скриптов);
2.	Пользователь в клиентской консоли указывает числа и операции между ними (порядок и правила указания могут быть любыми, но обязательно их необходимо предоставить пользователю);
3.	Данные о числах и операциях отправляются на сервер;
4.	Сервер производит необходимые действия и отправляет результат на клиентскую часть;
5.	Клиент получает и отображает результат в консоли;
6.	При желании клиент повторяет шаги 2-5.
7.	Реализовать возможность запоминания предыдущего результата и работы с ним при выполнении дальнейших операций;
8.	Реализовать на серверной части очередь FIFO для выполнения операций (т.е. работу с несколькими клиентами в порядке очереди);
9.	Расширить обычную очередь на очередь с приоритетами.

---

### Примечания:
*	Использование eval запрещено;
*	Сервер и клиент должны быть отдельными, работающими автономно, приложениями (можно писать их в одном проекте, но каждое должно работать автономно);
*	Общение между клиентом и сервером должно идти через Ethernet по UDP протоколу (разрешена реализация в локальной сети "127.0.0.1");
*	Постарайтесь сделать задание максимально полно со всеми необходимыми проверками ввода и вывода (т.е., например, если операция сложения между числами не поддерживается, то при вводе операции в консоль должно выводиться соответствующее сообщение. Или добавлять поддержку операции);
*	Отдавайте предпочтения не сторонним библиотекам, а собственным реализациям требуемого функционала.

---

### На что будет обращаться внимание:
*	Эффективность использования трафика;
*	Полнота реализации;
*	Стиль написания кода;
*	Архитектура кода;
*	Использованные решения/алгоритмы.

Решение ожидается в виде архива с проектом.

---

### Перед тем, как начать

#### Клонирование репозитория

Клонируйте репозиторий на свой локальный компьютер с помощью  
`git clone https://github.com/edenhauss/quanttelecom-test.git`

#### Настройка settings.py

```
server_ip = <ip-адрес сервера> # по умолчанию - 127.0.0.1
server_port = <порт сервера> # по умолчанию - 50000
```

#### Необходимо установить:

* [Python 3.10.x](https://www.python.org/downloads/release/python-3100/)

#### Запуск сервера

Запустите server.py, перейдя в его местоположение:
```
python server.py
```

#### Подключение к серверу

Запустите client.py, перейдя в его местоположение:
```
python client.py
```

#### Использование калькулятора

Соблюдайте формат ввода:

* <число1> <знак операции> <число2>
* \> <знак операции> <число> (если нужно работать с предыдущим результатом)

Доступные операции:

* сложение
* вычитание
* умножение
* деление
* поиск остатка
* деление нацело
* возведение в степень