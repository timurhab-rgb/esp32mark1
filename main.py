# main.py - основной код бота для управления светодиодом

from machine import Pin
import network
import utime
from config import utelegram_config, wifi_config
import utelegram  # Эту библиотеку мы скачаем отдельно

# Настройка пина для светодиода
# На многих платах ESP32 встроенный светодиод на пине 2 (GPIO2)
# Если у тебя внешний светодиод подключен к другому пину, замени 2 на свой номер
led = Pin(2, Pin.OUT)
led.value(0)  # Начальное состояние - выключен

# --- Подключение к WiFi ---
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
print("Подключаюсь к WiFi...")
sta_if.connect(wifi_config['ssid'], wifi_config['password'])

# Ждем подключения (таймаут 10 секунд)
timeout = 10
while not sta_if.isconnected() and timeout > 0:
    print(".")
    utime.sleep(1)
    timeout -= 1

if sta_if.isconnected():
    print("WiFi подключен!")
    print("Мой IP адрес:", sta_if.ifconfig()[0])  # Здесь ты увидишь IP в консоли Thonny
else:
    print("Не удалось подключиться к WiFi. Проверь настройки в config.py")
    # Можно добавить мигание светодиодом для сигнала ошибки
    while True:
        led.value(1)
        utime.sleep(0.2)
        led.value(0)
        utime.sleep(0.2)

# --- Функции-обработчики команд бота ---
def led_on(message):
    """Включает светодиод"""
    led.value(1)
    bot.send(message['message']['chat']['id'], 'turn on')
    print("Свет включен по команде")  # Для отладки в консоли Thonny

def led_off(message):
    """Выключает светодиод"""
    led.value(0)
    bot.send(message['message']['chat']['id'], 'turn off')
    print("Свет выключен по команде")

def start(message):
    """Приветственное сообщение"""
    bot.send(message['message']['chat']['id'], 
             'Hello.\n'
             '/led_on - turn on\n'
             '/led_off - turn off')

# --- Запуск бота ---
if sta_if.isconnected():
    # Создаем экземпляр бота
    bot = utelegram.ubot(utelegram_config['token'])
    
    # Регистрируем команды
    bot.register('/start', start)
    bot.register('/led_on', led_on)
    bot.register('/led_off', led_off)
    
    print('Бот запущен и готов к работе. Жду команды...')
    
    # Запускаем прослушивание (это бесконечный цикл)
    try:
        bot.listen()
    except Exception as e:
        print("Ошибка в работе бота:", e)
        print("Перезагрузка через 5 секунд...")
        utime.sleep(5)
        machine.reset()  # Перезагружаем ESP32 при ошибке
else:
    print("Нет подключения к интернету. Бот не запущен.")