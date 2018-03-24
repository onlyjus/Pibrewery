# Pibrewery
Pibrewery is a program to manage the brewing process.

## Software

### Dependencies

The following dependencies need to be installed:

- python
- kivy
- kivy-garden graph
- Adafruit_GPIO

To install kivy on the raspberry pi, please follow the instructions here:

https://kivy.org/docs/api-kivy.garden.html

To install kivy-garden run:

    $ pip install kivy-garden

Once kivy-garden is installed, install graph with:

    $ garden install graph

To install the Adafruit_GPIO library, please follow the instructions here:

https://github.com/adafruit/Adafruit_Python_GPIO

### Install
To install this software, clone the repository in your usr directory:

    $ cd
    $ git clone https://github.com/onlyjus/Pibrewery
    $ cd Pibrewery

Once the repository has been cloned, the application can be started with:

    $ python -m pibrewery

## Hardware

### ADC
In order to read sensors, like a thermister, on the raspberry pi, an analog to
digita converter (ADC) is needed. For this project, I used an ADS1115 from
adafruit. It is a 16 bit I2C ADC PGA.

## Contributors
- Justin Weber
