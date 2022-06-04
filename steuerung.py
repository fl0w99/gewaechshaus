from machine import Pin, SoftI2C
from time import sleep, sleep_ms
import onewire
import ds18x20
import ssd1306
import freesans20
import writer


# Manuelle Definitionen
ds_pin 		= Pin(13)           
relay_pin 	= 27                
scl_pin		= Pin(25)           
sda_pin     = Pin(14)           

oben_pin 	= 34                                  
unten_pin 	= 35                 
autom_pin 	= 32                                               
manuell_pin = 33                  

temperatur	= 10
modus = 0               #speichert aktuellen modus

# OLED Interface
i2c = SoftI2C(scl = scl_pin, sda = sda_pin)
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

        
        


def wait():

    oled.fill(0)    
    font_writer = writer.Writer(oled, freesans20)
    font_writer.set_textpos(oled, 5, 45)
    font_writer.printstring("Bitte")
    font_writer.set_textpos(oled, 30, 30)
    font_writer.printstring("Warten!")
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
    font_writer.set_textpos(oled, 25, 40)
    font_writer.printstring("Fehler")
    oled.show()

def oeffnen():

    oled.fill(0)    
    font_writer = writer.Writer(oled, freesans20)
    font_writer.set_textpos(oled, 25, 35)
    font_writer.printstring("Oeffnen")
    oled.show()
    sleep(3)

def schliessen():

    oled.fill(0)    
    font_writer = writer.Writer(oled, freesans20)
    font_writer.set_textpos(oled, 25, 20)
    font_writer.printstring("Schliessen")
    oled.show()
    sleep(3)
   
    
    

def messung():
    oled.fill(0)
    

    x = True                                                            # Optional (soll hinterher bei schalterbetätigung verändert werden, 
                                                                        # dann aus While True raus springen und in der anderen einmal schleife wird x wieder True gesetzt und die funktion neu gestartet)

    while x:                                                            # Vorher stand hier while true:
        status_manuell = mode_manuell.value()
        
        print('Automatik aktiv')
	
        if status_manuell != 1: 

            ds_sensor.convert_temp()
            sleep_ms(750)

            for rom in roms:

                temp = str(round(ds_sensor.read_temp(rom), 2))
                oled.fill(0)
                oled.text("Temperatur",25,0)
                oled.line (5,12,123,12,3)
                oled.text("Temperatur",25,0)
                oled.line (5,12,123,12,3)
                font_writer = writer.Writer(oled, freesans20)
                font_writer.set_textpos(oled, 25, 35)
                font_writer.printstring(temp + " C")
                print(ds_sensor.read_temp(rom))
                oled.show()
		
                if round(ds_sensor.read_temp(rom), 2) >= temperatur:	# Hier wird die Temperatur überprüft
                    relay.value(1)					                    # Fenster Öffnen
                else:
                    relay.value(0)					                    # Fenster schließen

        # if Abfrage für Manuell oder Automatik            
        elif status_manuell == 1:                                       # -- Modus Wahlschalter
            print('Manuell aktiv')		
            schleife = 1    
            oled.fill(0)    
            font_writer = writer.Writer(oled, freesans20)
            font_writer.set_textpos(oled, 25, 35)
            font_writer.printstring("Manuell")
            oled.show()
            sleep(3)

		
            while schleife == 1:                                        #-- muss auch beendet werden, wenn Mode geändert wird
                
                status_autom = mode_autom.value()
                status_oben = schalter_oben.value()
                status_unten = schalter_unten.value()

                if status_oben == 1:
                    relay.value(1)				                        # Überprüfen, dass Relais bei NO. Fenster schließt. Hier sollte es öffnen
                    print('Fenster öffnen')
                    oeffnen()
                    wait()
                

                elif status_unten == 1:
                    relay.value(0)				                        # Fenster sollte schließen
                    print('Fenster schließen')
                    schliessen()
                    wait()
        
                elif status_autom == 1:
                    schleife = 0
                    oled.fill(0)
                    oled.show()



    sleep(4)

    oled.fill(0)
    oled.show()
