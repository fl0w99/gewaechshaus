from machine import Pin, SoftI2C
from time import sleep, sleep_ms
import onewire, ds18x20
import ssd1306
import freesans20
import writer


# Manuelle Definitionen
ds_pin 		= Pin(19)
relay_pin 	= 21
oben_pin 	= 21
unten_pin 	= 21
autom_pin 	= 21
manuell_pin 	= 21
i2c_pin		= Pin(21)

temperatur	= 10



# OLED Interface
i2c = SoftI2C(scl = i2c_pin, sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)


# Temperatur Sensor Interface
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()


# Definition Relais
relay = Pin(relay_pin, Pin.OUT)


# Definition der Schalter
schalter_oben 	= Pin(oben_pin, Pin.IN)
schalter_unten 	= Pin(unten_pin, Pin.IN)
mode_autom 	= Pin(autom_pin, Pin.IN)
mode_manuell 	= Pin(manuell_pin, Pin.IN)

        
        

def pre():
    #OLED Anzeige
    oled.fill(0)

    oled.text("Temperatursensor",3,0)
    oled.text("- v0.1 -",38,20)
    oled.text("ESP32",48,50)
    oled.show()

    sleep(1)

    oled.fill(0)
    oled.text("Temperatur:",0,0)
    oled.text("10C",95,0)

    oled.text("Modus:",0,15)
    oled.text("Offen",80,15)

    oled.text("letzte Messung",8,40)
    oled.text("13C",50,52)
    oled.show()

    sleep(1)


def wait():

    oled.fill(0)    
    font_writer = writer.Writer(oled, freesans20)
    font_writer.set_textpos(oled, 25, 35)
    font_writer.printstring("Bitte Warten!")
    oled.show()

    sleep(10)

    oled.fill(0)    
    font_writer = writer.Writer(oled, freesans20)
    font_writer.set_textpos(oled, 25, 35)
    font_writer.printstring("Manuell")
    oled.show()



def fehler():

    oled.fill(0)    
    font_writer = writer.Writer(oled, freesans20)
    font_writer.set_textpos(oled, 25, 35)
    font_writer.printstring("Fehler")
    oled.show()
   
    
    

def messung():
    oled.fill(0)
    oled.text("Temperatur",25,0)
    oled.line (5,12,123,12,3)

    x = True                                                # Optional (soll hinterher bei schalterbetätigung verändert werden, 
                                                            # dann aus While True raus springen und in der anderen einmal schleife wird x wieder True gesetzt und die funktion neu gestartet)

    while x:                                                # Vorher stand hier while true:
        
        print('Automatik aktiv')
	
        if mode_autom == 1: 
            ds_sensor.convert_temp()
            sleep_ms(750)
            for rom in roms:
                temp = str(round(ds_sensor.read_temp(rom), 2))
                oled.fill(0)
                oled.text("Temperatur",25,0)
                oled.line (5,12,123,12,3)
                font_writer = writer.Writer(oled, freesans20)
                font_writer.set_textpos(oled, 25, 35)
                font_writer.printstring(temp + " C")
                print(ds_sensor.read_temp(rom))
                oled.show()
		
                if round(ds_sensor.read_temp(rom), 2) >= temperatur:	# Hier wird die Temperatur überprütf
                    relay.value(1)					# Fenster Öffnen
                else:
                    relay.value(0)					# Fenster schließen

        # if Abfrage für Manuell oder Automatik            
        elif mode_manuell == 1:                                         # -- Modus Wahlschalter
	    print('Manuelle aktiv')		
            schleife = 1    
                                   
                oled.fill(0)    
                font_writer = writer.Writer(oled, freesans20)
                font_writer.set_textpos(oled, 25, 35)
                font_writer.printstring("Manuell")
                oled.show()

		
            while schleife == 1:                                 #-- muss auch beendet werden, wenn Mode geändert wird
                
                if schalter_oben == 1:
                    relay.value(1)				# Überprüfen, dass Relais bei NO. Fenster schließt. Hier sollte es öffnen
                    print('Fenster öffnen')
                    wait()
                

                elif schalter_unten == 1:
                    relay.value(0)				# Fenster sollte schließen
                    print('Fenster schließen')
                    wait()
		
      
	
		elif mode_autom == 1:
		    schleife = 0
		    oled.fill(0)
		    oled.show()

        
        else:
            fehler()
            sleep(5)


    sleep(4)

    oled.fill(0)
    oled.show()




