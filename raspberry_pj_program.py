from tkinter import *
from gpiozero import LED,MotionSensor
import RPi.GPIO
from datetime import datetime as dt
from time import sleep

from multiprocessing import Process

import threading
import time

import paho.mqtt.client as mqtt

RPi.GPIO.setmode(RPi.GPIO.BCM)

led_1 = LED(14)
pir = MotionSensor(4)
gui = Tk()
gui.title("Smart Home Control")
gui.geometry("600x500")

text_duration = IntVar()
#exit event
exit_sleep_event = threading.Event()
exit_tracking_event = threading.Event()
exit_alarm_event = threading.Event()
record = []
#sleep mode
sleep_button = Button(gui,text = "Sleep", command  =lambda:OnButtonClick("sleep"),
                  bg = "bisque2",height=5,width = 10)
sleep_button.grid(row = 0, column = 1)
#turn off sleep mode
sleep_button_off = Button(gui,text = "Off", command  =lambda:OnButtonClick("sleep_off"),
                  bg = "bisque2",height=5,width = 10)
sleep_button_off.grid(row = 0, column = 2)
#sleep tracking function
sleep_button_tracking = Button(gui,text = "Tracking", command  =lambda:OnButtonClick("sleep_tracking"),
                  bg = "bisque2",height=5,width = 10)
sleep_button_tracking.grid(row = 0, column = 3)
#wake up function
wake_up_button = Button(gui,text = "Wake Up", command = lambda:OnButtonClick("wake_up"),
                      bg = "bisque2",height=5,width = 10)
wake_up_button.grid(row = 1,column =1)
#Security mode
security_button = Button(gui,text = "Security mode", command  =lambda:OnButtonClick("security"),
                  bg = "bisque2",height=5,width = 10)
security_button.grid(row = 2, column = 1)
security_button = Button(gui,text = "Security mode-off", command  =lambda:OnButtonClick("security_off"),
                  bg = "bisque2",height=5,width = 10)
security_button.grid(row = 2, column = 2)

on_button = Button(gui,text = "Light on", command  =lambda:OnButtonClick("light_on"),
                  bg = "bisque2",height=5,width = 10)
on_button.grid(row = 3, column = 0)

off_button = Button(gui,text = "Light off", command  =lambda:OnButtonClick("light_off"),
                  bg = "bisque2",height=5,width = 10)
off_button.grid(row = 3, column = 1)
label_sleep = Label(gui,
                 text = "welcome home")
label_sleep.grid(row = 4,column = 1)
#textbox
text_sleep = Entry(gui, width = 15)
text_sleep.grid(row = 0, column = 0)

text_wake = Entry(gui, width = 15)
text_wake.grid(row = 1, column = 0)

def sleep_mode():
    start_time = dt.now()
    led_1.off()
    exit_sleep_event.clear()
    while not exit_sleep_event.is_set():
        current = dt.now()
        duration = (current - start_time).seconds
        if duration == int(text_sleep.get()):
            exit_sleep_event.set()
            exit_tracking_event.set()
            print(5)
    led_1.on()

def sleep_tracking():
    movement_count = 0
    record = []
    while not exit_sleep_event.is_set():
        sleep(0.5)
        if pir.motion_detected:
            movement_count +=1
            current = dt.now().strftime('%Y-%m-%d %H:%M:%S')
            record.append((movement_count,current))
        
    print(record)
    if movement_count < 5:
        label_sleep.config (text = "well sleep")
    if movement_count >=5:
        label_sleep.config (text = f"you move {movement_count} while sleeping")

    sleep(3)
    label_sleep.config (text = "Welcome home")
#public data to cloud when system in security mode and motion is detected
def MQTT(msg): 
    ourClient=mqtt.Client("BachLuu_mqtt")
    ourClient.connect("test.mosquitto.org",1883)
    ourClient.subscribe("motion")
    ourClient.loop_start()
    # while 1:
    #     ourClient.publish("motion",msg)
    #     time.sleep(1)
    #     if (msg == "off"):
    #         print(1)
    #         break
    ourClient.publish("motion",msg)
    if (msg == "off"):
        print("out")
    while 1:
        time.sleep(1)
    


def security_motion():
    exit_alarm_event.clear()
    
    while not exit_alarm_event.is_set():
        if (pir.motion_detected):
            print("motion detected")
            #threading.Thread(target  = MQTT("intruder")).start()
            MQTT("intruder")
        sleep(0.1)
def security_off():
    exit_alarm_event.set()
    MQTT("off")

def wake_up():
    led_1.on()
    exit_sleep_event.set()

def close():
    RPi.GPIO.cleanup()
    gui.destroy()
    
def OnButtonClick(button_id):
    
    if button_id == "sleep":
        t1 = threading.Thread(target = sleep_mode)
        t1.start()
    if button_id == "sleep_off":
        exit_sleep_event.set()
    if button_id == "sleep_tracking":
        
        t1 = threading.Thread(target = sleep_mode)
        
        t2 = threading.Thread(target = sleep_tracking)
        #t1 = Process(target = sleep_mode)
        #t2 = Process(target = sleep_tracking)
        t1.start()
        t2.start()
        
 
    if button_id == "wake_up":
        wake_up()

    if button_id == "security":
        
        t = threading.Thread(target = security_motion)
        t.start()
    if button_id == "security_off":
        
        threading.Thread(target = security_off).start()
    if button_id == "light_on":
        led_1.on()
    if button_id == "light_off":
        led_1.off()
    

gui.protocol("WM_DELETE_WINDOW",close)
gui.mainloop()

