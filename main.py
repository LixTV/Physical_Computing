from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD

firmware_url = "https://raw.githubusercontent.com/LixTV/Physical_Computing/"

ota = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")

ota.download_and_install_update_if_available()


import time
import random
import machine
from neopixel import Neopixel
from lsm6dsox import LSM6DSOX
from machine import Pin, I2C

#--------Lage Sensor (I2C) - Funktionierend aus lage.py---------------
# Initialize the LSM6DSOX sensor with I2C interface (funktioniert aus lage.py)
try:
    lsm = LSM6DSOX(I2C(0, scl=Pin(13), sda=Pin(12)))
    print("LSM6DSOX Sensor initialisiert")
except Exception as e:
    print("Sensor Fehler")


#-------------------------------

#___________________________Funktionen____________________________

#Wurfel Seitenanzeige

def wurfel_create(flaeche,pos_wurf_x,pos_wurf_y):
        for x in range(2):
            for y in range(2):
                pixel.set_pixel(cube[flaeche][pos_wurf_x+x][pos_wurf_y+y], (0, 0, 255))
        
          
def wurfel_anzeige():
    #Fläche 1
    #mitte
    wurfel_create(0,3,3)
    
    #Fläche 2
    #l u
    wurfel_create(1,0,0)
    #r o
    wurfel_create(1,6,6)
    
    #Fläche 3
    #l u
    wurfel_create(2,0,0)
    #m
    wurfel_create(2,3,3)
    #r o
    wurfel_create(2,6,6)

    #Fläche 4
    #l u
    wurfel_create(2,0,0)
    #l o
    wurfel_create(2,0,6)
    #r u
    wurfel_create(2,6,0)
    #r o
    wurfel_create(2,6,6)
    
    #Fläche 5
    #l u
    wurfel_create(2,0,0)
    #l o
    wurfel_create(2,0,6)
    #r u
    wurfel_create(2,6,0)
    #r o
    wurfel_create(2,6,6)
    #m
    wurfel_create(2,3,3)
    
    #Fläche 4
    #l u
    wurfel_create(2,0,0)
    #l m
    wurfel_create(2,0,3)    
    #l o
    wurfel_create(2,0,6)
    #r u
    wurfel_create(2,6,0)
    #r m
    wurfel_create(2,6,3)
    #r o
    wurfel_create(2,6,6)
    
    
        


#___________generate Fruit________________    
def generate_fruit_position(snake, NUMPIXELS):
    attempts = 0
    while attempts < 100:  # Vermeide Endlosschleifen
        fruit_pos = random.randint(0, NUMPIXELS - 1)
        if fruit_pos not in snake:
            if fruit_pos not in fruit:
                return fruit_pos
        attempts += 1
    return 0  # Fallback

# Konfiguration
PIXEL_PIN = 27  # GPIO Pin für NeoPixel (anstatt board.A1)
COLOR = (30, 0, 0)  # Grundfarbe
COLOR_SNAKE = (10, 0, 0)  # Snake Farbe
COLOR_HEAD = (10, 10, 0)  # Snake Kopf Farbe
COLOR_FRUIT = (0, 10, 0)  # Frucht Farbe
CLEAR = (0, 0, 0)  # Aus/Leer
DELAY = 1  # Spielgeschwindigkeit in Sekunden
THRESH = 0.4  # Sensor Schwellwert
NUM_FRUITS = 10  # Anzahl Früchte
NUMPIXELS = 192  # Gesamtzahl LEDs (3 Seiten × 8×8)

# NeoPixel Setup (verwende deine neopixel.py Bibliothek)
pixel = Neopixel(NUMPIXELS, 0, PIXEL_PIN, "RGB")
pixel.brightness(50)

print("3D Snake Spiel gestartet...")
print(f"LEDs: {NUMPIXELS}, Früchte: {NUM_FRUITS}")

# WÜRFEL MATRIX [Seitenfläche][X-Koordinate][Y-Koordinate]
cube_C1 = [[[0 for y in range(8)] for x in range(8)] for f in range(3)]
cube = [[[0 for y in range(8)] for x in range(8)] for f in range(6)]
counter = 0
seite = 0

for y in range(8):
    for x in range(24):
        if x < 8:
            seite = 0
        elif x < 16:
            seite = 1
        else:
            seite = 2
        
        if y % 2 == 0:
            cube_C1[seite][x % 8][y] = counter
        else:
            cube_C1[seite][x % 8][y] = cube_C1[seite][x % 8][y-1] + 48 - 1 - 2*x
        counter = counter + 1

#cube inizilize
counter_cube = 0
for c in range(2):
    if c==0:
        for y in range(8):
            for x in range(24):
                if x < 8:
                    seite = 0
                elif x < 16:
                    seite = 1
                else:
                    seite = 2
        
                if y % 2 == 0:
                    cube[seite][x % 8][y] = counter_cube
                else:
                    cube[seite][x % 8][y] = cube[seite][x % 8][y-1] + 48 - 1 - 2*x
                counter_cube = counter_cube + 1
    if c==1:
        for y in range(8):
            for x in range(24):
                if x < 8:
                    seite = 5
                elif x < 16:
                    seite = 4
                else:
                    seite = 6
        
                if y % 2 == 0:
                    cube[seite][x % 8][y] = counter_cube
                else:
                    cube[seite][x % 8][y] = cube[seite][x % 8][y-1] + 48 - 1 - 2*x
                counter_cube = counter_cube + 1


print("LED-Würfel Matrix initialisiert")

# Snake Startposition
f_pos = 1  # Seitenfläche
x_pos = 3  # X-Position
y_pos = 4  # Y-Position

# SNAKE erzeugen
snake = []
snake.append(cube_C1[f_pos][x_pos+4][y_pos])
snake.append(cube_C1[f_pos][x_pos+3][y_pos])
snake.append(cube_C1[f_pos][x_pos+2][y_pos])
snake.append(cube_C1[f_pos][x_pos+1][y_pos])
snake.append(cube_C1[f_pos][x_pos][y_pos])

# Schlange zeichnen
for s in snake:
    pixel.set_pixel(s, COLOR_SNAKE)
pixel.show()

print("Snake initialisiert")
time.sleep(2)

# FRÜCHTE erzeugen
fruit = []
for i in range(NUM_FRUITS):
    fruit.append(generate_fruit_position(snake, NUMPIXELS))

for f in fruit:
    pixel.set_pixel(f, COLOR_FRUIT)
pixel.show()

print(f"{len(fruit)} Früchte platziert")

# Bewegungsrichtungen
richtung = "links"
rechts = False
links = True
oben = False
unten = False
richtung_bewegt = False

print("Spiel läuft - bewege den Würfel um zu steuern!")
print("Drücke Ctrl+C zum Beenden")

# Hauptspiel-Loop
try:
    while True:
        wurfel_anzeige()
        """
        #Fläche1
        for x in range(2):
            for y in range(2):
                pixel.set_pixel(cube_C1[0][x][y], (0, 0, 255))
        
                
                
        pixel.set_pixel(cube_C1[0][3][3], (0, 0, 255))
        pixel.set_pixel(cube_C1[0][3][4], (0, 0, 255))
        pixel.set_pixel(cube_C1[0][4][3], (0, 0, 255))
        pixel.set_pixel(cube_C1[0][4][4], (0, 0, 255))

        #Fläche2
        pixel.set_pixel(cube_C1[1][2][2], (0, 0, 255))
        pixel.set_pixel(cube_C1[1][2][3], (0, 0, 255))
        pixel.set_pixel(cube_C1[1][2][4], (0, 0, 255))
        pixel.set_pixel(cube_C1[1][2][5], (0, 0, 255))

        pixel.set_pixel(cube_C1[1][4][2], (0, 0, 255))
        pixel.set_pixel(cube_C1[1][4][3], (0, 0, 255))
        pixel.set_pixel(cube_C1[1][4][4], (0, 0, 255))
        pixel.set_pixel(cube_C1[1][4][5], (0, 0, 255))

        #Fläche3
        """
        
        # Beschleunigungsdaten lesen (wie in lage.py - funktioniert!)
        accel_values = lsm.accel()
        accel_x, accel_y, accel_z = accel_values
        
        # Optional: Gyroscope Daten auch verfügbar
        # gyro_values = lsm.gyro()
        # gyro_x, gyro_y, gyro_z = gyro_values
        
        # Debug Output (optional)
        # print('Accelerometer: x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*accel_values))
        
        # Normalisierung für Bewegungssteuerung
        accel_x_norm = accel_x 
        accel_y_norm = accel_y 
        accel_z_norm = accel_z
        
        print("x:",accel_x_norm,"y:",accel_y_norm,"z:",accel_z_norm)

        # RECHTS bewegen
        if ((accel_x_norm >= THRESH and richtung_bewegt == False) or 
            (rechts == True and -THRESH <= accel_x_norm <= THRESH and -THRESH <= accel_y_norm <= THRESH)):
            
            if cube_C1[f_pos][x_pos][y_pos] < NUMPIXELS - 1:
                if x_pos == 7:
                    if f_pos == 2:
                        f_pos = 0
                    else:
                        f_pos += 1
                    x_pos = 0
                else:
                    x_pos += 1
                
                snake.append(cube_C1[f_pos][x_pos][y_pos])
            
            rechts, links, oben, unten = True, False, False, False
            richtung_bewegt = True

        # LINKS bewegen
        elif ((accel_x_norm <= -THRESH and richtung_bewegt == False) or 
              (links == True and -THRESH <= accel_x_norm <= THRESH and -THRESH <= accel_y_norm <= THRESH)):
            
            if cube_C1[f_pos][x_pos][y_pos] < NUMPIXELS + 1:
                if x_pos == 0:
                    if f_pos == 0:
                        f_pos = 2
                    else:
                        f_pos -= 1
                    x_pos = 7
                else:
                    x_pos -= 1
                
                snake.append(cube_C1[f_pos][x_pos][y_pos])
            
            rechts, links, oben, unten = False, True, False, False
            richtung_bewegt = True

        # OBEN bewegen
        elif ((accel_y_norm >= THRESH and richtung_bewegt == False) or 
              (oben == True and -THRESH <= accel_x_norm <= THRESH and -THRESH <= accel_y_norm <= THRESH)):
            
            if cube_C1[f_pos][x_pos][y_pos] < NUMPIXELS - 1:
                if y_pos == 7:
                    print("Oben: Übergang zu anderer Fläche noch nicht implementiert")
                else:
                    y_pos += 1
                
                snake.append(cube_C1[f_pos][x_pos][y_pos])
            
            rechts, links, oben, unten = False, False, True, False
            richtung_bewegt = True

        # UNTEN bewegen
        elif ((accel_y_norm <= -THRESH and richtung_bewegt == False) or 
              (unten == True and -THRESH <= accel_x_norm <= THRESH and -THRESH <= accel_y_norm <= THRESH)):
            
            if cube_C1[f_pos][x_pos][y_pos] < NUMPIXELS - 1:
                if y_pos == 0:
                    print("Unten: Übergang zu anderer Fläche noch nicht implementiert")
                else:
                    y_pos -= 1
                
                snake.append(cube_C1[f_pos][x_pos][y_pos])
            
            rechts, links, oben, unten = False, False, False, True
            richtung_bewegt = True

        richtung_bewegt = False

        # Kollisionserkennung (Snake beißt sich selbst)
        current_pos = cube_C1[f_pos][x_pos][y_pos]
        for s in snake[:-1]:
            if current_pos == s:
                print("GAME OVER - Snake hat sich selbst gebissen!")
                # Game Over Animation
                for x in range(8):
                    for y in range(8):
                        pixel.set_pixel(cube_C1[1][x][y], (0, 10, 0))
                pixel.show()
                time.sleep(3)
                
                # LEDs löschen
                for x in range(8):
                    for y in range(8):
                        pixel.set_pixel(cube_C1[1][x][y], CLEAR)
                pixel.show()

        # Snake Kopf zeichnen
        pixel.set_pixel(snake[-1], COLOR_SNAKE)

        # Frucht essen prüfen
        eating = any(current_pos == f for f in fruit)

        if eating:
            print("Frucht gegessen! Snake wächst")
            fruit.remove(current_pos)
            
            if len(snake) < NUMPIXELS - NUM_FRUITS:
                new_fruit = generate_fruit_position(snake, NUMPIXELS)
                fruit.append(new_fruit)
                pixel.set_pixel(new_fruit, COLOR_FRUIT)
        else:
            # Schwanz löschen (nur wenn keine Frucht gegessen)
            tail = snake.pop(0)
            pixel.set_pixel(tail, CLEAR)

        pixel.show()
        time.sleep(DELAY)

except KeyboardInterrupt:
    print("\nSpiel beendet")
    pixel.clear()
    pixel.show()
    print("Alle LEDs ausgeschaltet")

