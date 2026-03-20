# main.py - основной код бота для управления светодиодом

from machine import Pin
import network
import utime
from config import utelegram_config, wifi_config
import utelegram  # Эту библиотеку мы скачаем отдельно


led = Pin(2, Pin.OUT)
led.value(0)  

# Подключение к WiFi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
print("Подключаюсь к WiFi...")
sta_if.connect(wifi_config['ssid'], wifi_config['password'])


timeout = 10
while not sta_if.isconnected() and timeout > 0:
    print(".")
    utime.sleep(1)
    timeout -= 1

if sta_if.isconnected():
    print("WiFi подключен!")
    print("Мой IP адрес:", sta_if.ifconfig()[0])  
else:
    print("Не удалось подключиться к WiFi. Проверь настройки в config.py")
    while True:
        led.value(1)
        utime.sleep(0.2)
        led.value(0)
        utime.sleep(0.2)

# Функции-обработчики команд бота
def led_on(message):
    led.value(1)
    bot.send(message['message']['chat']['id'], 'turn on')
    print("Свет включен по команде")  

def led_off(message):
    led.value(0)
    bot.send(message['message']['chat']['id'], 'turn off')
    print("Свет выключен по команде")

def start(message):
    bot.send(message['message']['chat']['id'], 
             'Hello.\n'
             '/led_on - turn on\n'
             '/led_off - turn off')

# Запуск бота
if sta_if.isconnected():
    bot = utelegram.ubot(utelegram_config['token'])
    
    bot.register('/start', start)
    bot.register('/led_on', led_on)
    bot.register('/led_off', led_off)
    
    print('Бот запущен и готов к работе. Жду команды...')
    
    try:
        bot.listen()
    except Exception as e:
        print("Ошибка в работе бота:", e)
        print("Перезагрузка через 5 секунд...")
        utime.sleep(5)
        machine.reset()  
else:
    print("Нет подключения к интернету. Бот не запущен.")