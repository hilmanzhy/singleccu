import pygame
import time
import threading
import RPi.GPIO as GPIO
import smbus
import ConfigParser
from ConfigParser import SafeConfigParser
bus0 = smbus.SMBus(1)

MHD_R = 0x2B
NHD_R = 0x2C
NCL_R = 0x2D
FDL_R = 0x2E
MHD_F = 0x2F
NHD_F = 0x30
NCL_F = 0x31
FDL_F = 0x32
ELE0_T = 0x41
ELE0_R = 0x42
ELE1_T = 0x43
ELE1_R = 0x44
ELE2_T = 0x45
ELE2_R = 0x46
ELE3_T = 0x47
ELE3_R = 0x48
ELE4_T = 0x49
ELE4_R = 0x4A
ELE5_T = 0x4B
ELE5_R = 0x4C
ELE6_T = 0x4D
ELE6_R = 0x4E
ELE7_T = 0x4F
ELE7_R = 0x50
ELE8_T = 0x51
ELE8_R = 0x52
ELE9_T = 0x53
ELE9_R = 0x54
ELE10_T = 0x55
ELE10_R = 0x56
ELE11_T = 0x57
ELE11_R = 0x58

FIL_CFG = 0x5D
ELE_CFG = 0x5E
GPIO_CTRL0 = 0x73
GPIO_CTRL1 = 0x74
GPIO_DATA = 0x75
GPIO_DIR = 0x76
GPIO_EN = 0x77
GPIO_SET = 0x78
GPIO_CLEAR = 0x79
GPIO_TOGGLE = 0x7A
ATO_CFG0 = 0x7B
ATO_CFGU = 0x7D
ATO_CFGL = 0x7E
ATO_CFGT = 0x7F

TOU_THRESH = 5
REL_THRESH = 6


def readData0(address):
    touchData0 = bus0.read_word_data(address, 0x00)
    return touchData0


def setup0(address):
    bus0.write_byte_data(address, ELE_CFG, 0x00)
    bus0.write_byte_data(address, MHD_R, 0x01)
    bus0.write_byte_data(address, NHD_R, 0x01)
    bus0.write_byte_data(address, NCL_R, 0x00)
    bus0.write_byte_data(address, FDL_R, 0x00)
    bus0.write_byte_data(address, MHD_F, 0x01)
    bus0.write_byte_data(address, NHD_F, 0x01)
    bus0.write_byte_data(address, NCL_F, 0xFF)
    bus0.write_byte_data(address, FDL_F, 0x02)

    bus0.write_byte_data(address, ELE0_T, TOU_THRESH)
    bus0.write_byte_data(address, ELE0_R, REL_THRESH)
    bus0.write_byte_data(address, ELE1_T, TOU_THRESH)
    bus0.write_byte_data(address, ELE1_R, REL_THRESH)
    bus0.write_byte_data(address, ELE2_T, TOU_THRESH)
    bus0.write_byte_data(address, ELE2_R, REL_THRESH)
    bus0.write_byte_data(address, ELE3_T, TOU_THRESH)
    bus0.write_byte_data(address, ELE3_R, REL_THRESH)
    bus0.write_byte_data(address, ELE4_T, TOU_THRESH)
    bus0.write_byte_data(address, ELE4_R, REL_THRESH)
    bus0.write_byte_data(address, ELE5_T, TOU_THRESH)
    bus0.write_byte_data(address, ELE5_R, REL_THRESH)
    bus0.write_byte_data(address, ELE6_T, TOU_THRESH)
    bus0.write_byte_data(address, ELE6_R, REL_THRESH)
    bus0.write_byte_data(address, ELE7_T, TOU_THRESH)
    bus0.write_byte_data(address, ELE7_R, REL_THRESH)
    bus0.write_byte_data(address, ELE8_T, TOU_THRESH)
    bus0.write_byte_data(address, ELE8_R, REL_THRESH)
    bus0.write_byte_data(address, ELE9_T, TOU_THRESH)
    bus0.write_byte_data(address, ELE9_R, REL_THRESH)
    bus0.write_byte_data(address, ELE10_T, TOU_THRESH)
    bus0.write_byte_data(address, ELE10_R, REL_THRESH)
    bus0.write_byte_data(address, ELE11_T, TOU_THRESH)
    bus0.write_byte_data(address, ELE11_R, REL_THRESH)

    bus0.write_byte_data(address, FIL_CFG, 0x04)
    bus0.write_byte_data(address, ELE_CFG, 0x0C)


def onoffsection():
    print("sectionantidulu")


TOU_THRESH = 5
REL_THRESH = 6
setup0(0x5a)
last_touched0 = readData0(0x5a)

lastTap0 = 0
pin = 0

while True:
    currentTap0 = readData0(0x5a)
    for i in range(1, 8):
        pin_bit0 = 1 << i
        if currentTap0 & pin_bit0 and not lastTap0 & pin_bit0:
            print("Touched: ", i)

        if not currentTap0 & pin_bit0 and lastTap0 & pin_bit0:
            print("Released: ", i)
    lastTap0 = currentTap0
    time.sleep(0.1)
