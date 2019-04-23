### Бот для отправки скриншотов из графаны в телеграм.

#### Начало работы

**Склонируйте репозиторий:** 
https://github.com/raptor72/GrafanaScreen-TlgBot

Для рендеринга картинок по API графаны необходимо сгенерировать ключ.
Поместите его в **config.py** в место **grafana_token**.

Если для доступа в телеграм будет использоваться прокси, укажите его в **apihelper_proxy**.
Если вы не используете прокси, закомментируйте строку 15 в **main.py**:

    apihelper.proxy = apihelper_proxy

Укажите **image_path**. Это папка в которую будут загружаться скриншоты из графаны.
Пользователь, под которыйм будет запущен скрипт должен иметь права на эту папку.

Ссылка на используемую графану:

    grafana_url

Токен телеграм бота:

    bot_token

Cпискок пользователей, которые смогут использовать бот:

    user_list

Если использование бота не нужно ограничивать списком пользователей, 
то поменятйте опцию: 

    check = 0

Cписок комманд, которые понимает бот: 

    command_list

Данный список содержит названия дашбордов и графиков. В примере используются два дашборда **bot-testing-dashboard** и **open-dashboard**.
Они включают в  себя по 2 графика: **Carbon - agents localdomain**, **Metric recieved** и **Commited points** и **MemUssage**.

Названия дашбордов в **command_list** необходимо внести так как они называются. Названия графиков можно задать произвольно,
но необходимо указать корректный **panelId** для конкретного графика.

Например график **Carbon - agents localdomain** имеет следующую ссылку:

http://192.168.231.6:3000/dashboard/db/bot-testing-dashboard?refresh=1m&panelId=1&fullscreen&orgId=1

В ней видно, что его **panelId=1** 

и это указано в соответствующем блоке **main.py**:

```python
dashboard = 'bot-testing-dashboard'
if message.text == 'Carbon agents localdomain':
    panelId = ('1')
```

Ссылки:
1. https://github.com/eternnoir/pyTelegramBotAPI
2. https://grafana.com/docs/http_api/auth/
