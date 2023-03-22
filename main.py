import time
import httpx
import json
from sql_app import crud


def get_coordinate():
    """Функция получкения адреса от пользователя
    """
    coordinat_message = """
    Введите адрес для определения координат
    """
    print(coordinat_message)

    echo = input("Введите данные: ")
    try:
        settings = crud.select_settings()

        api = settings["api"]
        url = settings["url"]
        count = settings["count"]
        language = settings["language"]

    except Exception:
        print("Произошла ошибка в работе программы\nПроверьте настройки программы, вы допустили ошибку при вводе данных")
        return 'fail'

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Token " + api,
    }

    data = {
        "query": echo,
        "count": count,
        "language": language
    }

    coordinats = httpx.post(url, data=json.dumps(data), headers=headers)

    if coordinats.status_code == 200:
        print("Выберите нужный вам вариант, введите нужную цифру из представленного списка\nЕсли ни один из представленных вариантов вас не устривает введите exit")
        addresses = []

        for dat in coordinats.json()["suggestions"]:
            addresses.append(dat)
            print(addresses.index(dat), dat['value'])

        while True:
            echo = input("Введите нужный вам вариант: ")

            if echo == 'exit':
                print("Вы прервали поиск координат, можете попробовать заново")
                break
            try:

                check = addresses[int(echo)]
                geo_lat = check['data']['geo_lat']
                geo_lon = check['data']["geo_lon"]
                result = f"Координаты по адресу: {check['value']},\nШирота: {geo_lat},\nДолгота: {geo_lon}"

            except Exception:
                print("Вы ввели неккоректные данные, попробуйте снова")
                continue
            


            return result
            
    else:
        print(
            "Произошла ошибка в работе программы\nПроверьте настройки программы, возможно вы допустили ошибку при вводе данных\n"\
            "Также проверьте сервис dadata, возможно у них проводятся технические работы на сайте"
            )
        return 'fail'


def change_url():
    """ Функция для изменения URL
    """
    text_start = "Смена адреса\n"
    print(text_start)
    echo = input('Введите новый URL адрес: ')
    crud.new_url(echo)
    text_end = "### Адрес успешно изменен!"
    print(text_end)
    return 'ok'


def change_api():
    """ Функция для изменения API ключа
    """
    text_start = "Смена API ключа\n"
    print(text_start)
    echo = input('Введите новый API ключ: ')
    crud.new_api(echo)
    text_end = "### API ключ успешно изменен!"
    print(text_end)
    return 'ok'


def change_language():
    """ Функция для изменения языка ответа 
    """
    text_start = "Смена языка ответа от сервиса\n"
    print(text_start)
    echo = input('Введите `en` либо `ru`: ')
    if echo == 'en' or echo == 'ru':
        crud.new_language(echo)
    else:
        print("Вы ввели некорректные данные")
        return 'fail'
    text_end = "### Язык ответа успешно изменен!"
    print(text_end)
    return 'ok'


def change_count():
    """ Функция для изменения кол-ва вараинтов ответа
    """
    text_start = "Смена кол-ва вариантов ответа от сервиса\n"
    print(text_start)
    echo = input('Введите число от 1 до 20(включительно): ')
    if 20 > int(echo) > 0:

        try:
            int(echo)
            crud.new_count(echo)
            text_end = "### Кол-во вариантов ответов успешно изменено!"
            print(text_end)
        except:
            error = "Введенное значение не является числом!"
            print(error)
    else:
        print("Вы введи неккректные данные")
        return 'fail'

    return 'ok'


def show_settings():
    """ Функция для отображения текущих настроек
    """
    data_settings = crud.select_settings()
    text_show = f"Текущие настройки: \nURL: {data_settings['url']},\nAPI ключ: {data_settings['api']},\n"\
        f"Язык ответа: {data_settings['language']},\nКол-во вариантов ответа: {data_settings['count']}"
    
    print(text_show)
    return "ok"


def settings():
    """Функция меню настроек программы
    0 - Изменить базовый URL к сервису dadata
    1 - Добавить API ключ для сервиса dadata
    2 - Язык ответа от сервиса dadata
    3 - Изменение количесва вариантов ответа от сервиса dadata
    4 - Отобразить текущие настройки программы
    5 - Вернуться в главное меню
    """
    menu_messsage = """
    ###########################################################
    0 - Изменить базовый URL к сервису dadata
    1 - Добавить API ключ для сервиса dadata
    2 - Язык ответа от сервиса dadata
    3 - Изменение количества вариантов ответа от сервиса dadata
    4 - Отобразить текущие настройки программы
    5 - Вернуться в главное меню
    """
    while True:

        print(menu_messsage)
        echo = input('Введите команду: ')

        if echo == '0':

            change_url()
            
        elif echo == '1':

            change_api()

        elif echo == '2':

            change_language()

        elif echo == '3':

            change_count()

        elif echo == '4':

            show_settings()

        elif echo == '5':

            break
        else:
            print("Вы ввели неизвестную команду, Пожайлуста повторите попытку")


def main_menu():
    """Функция вызова меню
    Функционал меню:
    0 - Ввод адреса
    1 - Настройка программы
    2 - Сброс настроек программы
    3 - Выход из программы
    """
    first_message = """
        Здравствуйте, данная программа создана для получения координат определенного адреса.
    Для корректной работы программмы, при первом запуске необходимо настроить программу и 
    ввести необходимые данные, такие как: Базовый URL к сервису dadata(в программе задан по
    умолчанию), API ключ сервиса dadata, в скобках указан адрес, по которому необходимо
    зарегистрироваться и получить API ключ(https://dadata.ru/profile/#info) указать количество
    возможных вариантов координат по вашему запросу, выбрать язык на котором будет получен 
    ответ от сервиса dadata. Для перехода к настройкам введите цифру 1.
        Для получения координат введите цифру 0, после укажите адрес в произвольной форме
        Если во время работы программы вы получаете ошибку, то возможно вы настроили программу
    неправильно, рекомендуем вам сбросить настройки, для этого введите цифру 2
    Важно!!! После сброса настроек необходимо заново ввести API ключ. 
        Для выхода из программы введите цифру 3.
    """
    menu_message = """
    ##########################################################################################
    0 - Ввод адреса
    1 - Настройка программы
    2 - Сброс настроек программы
    3 - Выход из программы
    """
    print(first_message)
    while True:
        print(menu_message)

        echo = input("Введите команду: ")

        if echo == '0':

            print(get_coordinate())

        elif echo == '1':

            settings()

        elif echo == '2':

            crud.reset_settings()
            print("Настройки успешно сброшены до настроек по умолчанию")

        elif echo == '3':

            break

        else:
            print("Вы ввели неизвестную команду, Пожалуйста повторите попытку")
            

    print("Программа завершила свою работу")

if __name__ == "__main__":
    check_settings = crud.select_settings()
    if check_settings is None:
        crud.initial_app()
    main_menu()