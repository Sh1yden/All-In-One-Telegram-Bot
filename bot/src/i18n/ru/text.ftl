
# ? Service Msgs
message_service_in_development =
    👨‍💻⌛ Это функция еще в разработке. Мы добавим её позже, пожалуйста подождите.
message_service_error_not_edit = ❌ Сообщение нельзя изменить.
message_service_error_not_user_enable = ❌ Ошибка: не удалось определить пользователя.
message_service_error_not_found_in_service = ❌ Ошибка: не удалось получить данные от сервиса.


# ? BEFORE Start Msgs
message_before_start =
    Привет🗿👋!  Это бот🤖 All In One(Всё В Одном)📚.
    💼 Тут будет тест различных функций Aiogram и не только.
    ⛅️ Первая будет погода дальше что_нибудь еще(потом дополню это описание).
    🚀 ЗАПУСТИТЬ: /start.


# ? START Msgs
message_start_hello = Привет🗿👋
message_start_main_menu =
    !
    💼 Тут будет меню выбора различных функций бота.
    🚑 Так же чтобы вывести все команды бота напиши /help.
    ⛅️ Вызвать функцию погоды можно нажав кнопку ниже, либо же введя команду /weatherMenu.


# ? Help Msgs
message_help =
    🚑 Это меню помощи.📚 Тут будут все команды бота:
    🚀 Начальное меню /start.
    🚑 Вызвать это меню /help.
    ⛅️ Меню погоды /weatherMenu.


# ? WEATHER Msgs
# ? Weather MENU Msgs
message_weather_menu =
    ⛅️ Это меню погоды. Выбрать нужные функции💼 можно под сообщением или написав нужные команды📚.

# ? Weather NOW Msgs
emoji_weather_now_day = ☀️
emoji_weather_now_night = 🌙
message_weather_now_header =
    🌡 Погода в городе { $city } на { $time }{ $day_or_night_emoji }:

    ☯️ Средняя температура: { $avg_temp }{ $temp_unit }
    ☯️❗ Средняя температура без ошибочных данных: { $avg_filtered }{ $temp_unit }

    ⌛ Сейчас:

message_weather_now_source_template = { $num }. { $source_name }: { $temp }{ $temp_unit }
message_weather_now_summary_template =
    📖 Краткая сводка:
        🏙️ Условия: { $condition }
        👤 Ощущается как: { $feels_like }{ $temp_unit }
        💧 Влажность: { $humidity }{ $humidity_unit }
        🌬️ Ветер: { $wind }{ $wind_unit }

# ? Weather Codes
# ? Weather Codes WMO
message_weather_code_0 = Ясно
message_weather_code_1 = Преимущественно ясно
message_weather_code_2 = Переменная облачность
message_weather_code_3 = Пасмурно
message_weather_code_45 = Туман
message_weather_code_48 = Инейный туман
message_weather_code_51 = Морось слабая
message_weather_code_53 = Морось умеренная
message_weather_code_55 = Морось сильная
message_weather_code_56 = Ледяная морось слабая
message_weather_code_57 = Ледяная морось сильная
message_weather_code_61 = Дождь слабый
message_weather_code_63 = Дождь умеренный
message_weather_code_65 = Дождь сильный
message_weather_code_66 = Ледяной дождь слабый
message_weather_code_67 = Ледяной дождь сильный
message_weather_code_71 = Снег слабый
message_weather_code_73 = Снег умеренный
message_weather_code_75 = Снег сильный
message_weather_code_77 = Снежные зерна
message_weather_code_80 = Ливень слабый
message_weather_code_81 = Ливень умеренный
message_weather_code_82 = Ливень сильный
message_weather_code_85 = Снежный ливень слабый
message_weather_code_86 = Снежный ливень сильный
message_weather_code_95 = Гроза слабая
message_weather_code_96 = Гроза с градом
message_weather_code_99 = Гроза сильная с градом

# ? Weather Codes WeatherAPI
message_weather_code_1000 = Солнечно
message_weather_code_1003 = Местами облачно
message_weather_code_1006 = Облачно
message_weather_code_1009 = Пасмурно
message_weather_code_1030 = Туман
message_weather_code_1063 = Местами возможен дождь
message_weather_code_1066 = Местами возможен снег
message_weather_code_1069 = Местами возможна ледяная крупа
message_weather_code_1087 = Возможны грозовые вспышки
message_weather_code_1114 = Метель
message_weather_code_1117 = Снежная буря
message_weather_code_1135 = Туман
message_weather_code_1147 = Замерзающий туман
message_weather_code_1150 = Местами слабая морось
message_weather_code_1153 = Слабая морось
message_weather_code_1168 = Замерзающая морось
message_weather_code_1171 = Сильная замерзающая морось
message_weather_code_1180 = Местами слабый дождь
message_weather_code_1183 = Слабый дождь
message_weather_code_1186 = Умеренный дождь
message_weather_code_1189 = Сильный дождь
message_weather_code_1192 = Слабый дождь с туманом
message_weather_code_1195 = Умеренный или сильный дождь
message_weather_code_1198 = Слабый ледяной дождь
message_weather_code_1201 = Умеренный или сильный ледяной дождь
message_weather_code_1204 = Слабая ледяная крупа
message_weather_code_1207 = Умеренная или сильная ледяная крупа
message_weather_code_1210 = Местами слабый снег
message_weather_code_1213 = Слабый снег
message_weather_code_1216 = Местами умеренный снег
message_weather_code_1219 = Умеренный снег
message_weather_code_1222 = Местами сильный снег
message_weather_code_1225 = Сильный снег
message_weather_code_1237 = Ледяные гранулы
message_weather_code_1240 = Слабый дождевой ливень
message_weather_code_1243 = Умеренный или сильный дождевой ливень
message_weather_code_1246 = Проливной дождевой ливень
message_weather_code_1249 = Слабый ливень ледяной крупы
message_weather_code_1252 = Умеренный или сильный ливень ледяной крупы
message_weather_code_1255 = Слабый снежный ливень
message_weather_code_1258 = Умеренный или сильный снежный ливень
message_weather_code_1261 = Слабый ливень ледяных гранул
message_weather_code_1264 = Умеренный или сильный ливень ледяных гранул
message_weather_code_1273 = Местами слабый дождь с грозой
message_weather_code_1276 = Умеренный или сильный дождь с грозой
message_weather_code_1279 = Местами слабый снег с грозой
message_weather_code_1282 = Умеренный или сильный снег с грозой

# ? Weather Codes VisualCrossing (текстовые описания)
message_weather_code_clear = Ясно
message_weather_code_partly_cloudy = Местами облачно
message_weather_code_cloudy = Облачно
message_weather_code_overcast = Пасмурно
message_weather_code_fog = Туман
message_weather_code_rain = Дождь
message_weather_code_snow = Снег
message_weather_code_thunderstorm = Гроза
message_weather_code_mist = Мгла




# ? Device Msgs
message_device_select = ❓ Выберете свой девайс для определения местоположения.


# ? LOCATION Msgs

# ? Location COMMON Msgs
message_location_good_send =
    📍 Получено местоположение.
    Ваши координаты и город:
    🏙️ Город: { $city }
    ↔️ Широта: { $latitude }
    ↕️ Долгота: { $longitude }

# ? Location CURRENT Msgs
message_location_current = 📍 Текущая локация:

# ? Location PHONE Msgs
message_location_send_on_phone = ❗ Пожалуйста, отправьте ваше местоположение(через телеграм):

# ? Location PC Msgs
message_location_send_on_pc =
    ❗ Чтобы отменить напишите отмена. Пожалуйста, введите текстом ваше местоположение(Город):

# ? Location ERROR Msgs
message_location_cancel = ❌ Запрос локации отменен.
message_location_null_error =
    ⚠️ В ваших данных локации найдены пустые значения (NULL).
    Пожалуйста, обновите локацию заново:
message_location_save_error = ❌ Ошибка сохранения локации
message_location_not_posted = ❌ Локация не установлена
message_location_unknown_loc = ❓ Неизвестный тип локации
