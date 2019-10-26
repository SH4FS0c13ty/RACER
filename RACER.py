import pygame
import time
from random import*
import getpass
from subprocess import call

pygame.init()

# Define colors
blue = (113, 177, 227)
white = (255, 255, 255)
orange = (255, 83, 9)

# Variables for Easter Egg
g = 0
s = 0

# Window layout
surfaceW = 600
surfaceH = 800

surface = pygame.display.set_mode((surfaceW, surfaceH))
pygame.display.set_caption("Racer")
horloge = pygame.time.Clock()

# Importing car crash sound
crash = pygame.mixer.Sound('Res/Crash.ogg')

# Importing pictures
imgMenu = pygame.image.load('Res/Menu.png')
Background = pygame.image.load('Res/Road.png')
imgCar = pygame.image.load('Res/Main.png')
icon = pygame.image.load('Res/Icon.png')

# Set game icon
pygame.display.set_icon(icon)

# Importing car pictures
imgAmbulance = pygame.image.load('Res/Ambulance.png')
imgBlackViper = pygame.image.load('Res/Black_Viper.png')
imgMiniTruck = pygame.image.load('Res/Mini_Truck.png')
imgPolice = pygame.image.load('Res/Police.png')

# Get rectangles for previously imported pictures
imgrect = imgCar.get_rect()
imgAmbulanceRect = imgAmbulance.get_rect()
imgBlackViperRect = imgBlackViper.get_rect()
imgMiniTruckRect = imgMiniTruck.get_rect()
imgPoliceRect = imgPolice.get_rect()

# Score function
def score(compte):
    police = pygame.font.Font('Res/RoadTest.ttf', 40)
    texte = police.render("Passed cars: " + str(compte), True, orange)
    surface.blit(texte, [0, 0])

# Car spawns
def cars():
    surface.blit(imgAmbulance, imgAmbulanceRect)
    surface.blit(imgBlackViper, imgBlackViperRect)
    surface.blit(imgMiniTruck, imgMiniTruckRect)
    surface.blit(imgPolice, imgPoliceRect)


# Wait function for menu() and end()
def wait():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if(event.type == pygame.QUIT):
            pygame.quit()
            quit()
        elif(event.type == pygame.KEYUP):
            continue
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_SPACE):
                return event.key
            if(event.key == pygame.K_RETURN):
                pygame.quit()
                quit()

# Text object function
def creaTexteObj(texte, police):
    texteSurface = police.render(texte, True, orange)
    return texteSurface, texteSurface.get_rect()

# Message function for end()
def message(texte):
    GOTexte = pygame.font.Font('Res/RoadTest.ttf', 170)
    petitTexte = pygame.font.Font('Res/RoadTest.ttf', 30)

    GOTexteSurf, GOTexteRect = creaTexteObj(texte, GOTexte)
    GOTexteRect.center = 300, ((surfaceH / 2) - 50)
    surface.blit(GOTexteSurf, GOTexteRect)

    petitTexteSurf, petitTexteRect = creaTexteObj(
        "Press SPACE to restart or ENTER to quit", petitTexte)
    petitTexteRect.center = surfaceW / 2, ((surfaceH / 2) + 50)
    surface.blit(petitTexteSurf, petitTexteRect)
    pygame.mixer.music.stop()
    pygame.display.update()

    while wait() == None:
        horloge.tick()
    main()

# End function
def end():
    pygame.mixer.music.stop()
    crash.play()
    message("CRASH")

# Spawn THE car
def spawnCar(x, y, image):
    surface.blit(image, (x, y))

# Main function to make the game works
def main():

    # Define global variables x and y for cars
    global x_car, y_car, x2_car, y2_car, x3_car, y3_car
    global x4_car, y4_car

    # Define last variable to know which column was last used
    last = None

    # Play music (Happy Ape Rodeo by Shaka Ponk from the album The Black Pixel Ape)
    pygame.mixer.music.load('Res/Shaka_Ponk_-_Happy_Ape_Rodeo.ogg')
    pygame.mixer.music.play(-1)

    #Checking and changing score (easter egg)
    if(s != 0):
        current_score = s
    else:
        current_score = 0

    # Define rectangle coordinates for THE car
    imgrect.x = 250
    imgrect.y = 600

    # Define THE car movements
    y_mouvement = 0
    x_mouvement = 0

    # Define background movement
    x_BG = 0
    y_BG = -170

    # Define variable for game over check
    game_over = False

    # Define rectangles coordinates for cars
    imgAmbulanceRect.x = 10
    imgAmbulanceRect.y = -100
    imgBlackViperRect.x = 405
    imgBlackViperRect.y = -200
    imgMiniTruckRect.x = 210
    imgMiniTruckRect.y = -300
    imgPoliceRect.x = 510
    imgPoliceRect.y = -500

    # Define speed for background and cars
    BG_speed = 4
    car1_speed = 1
    car2_speed = 1.25
    car3_speed = 1.5
    car4_speed = 1

    # Checking for game over and starting game
    while not game_over:
        # Check for events
        for event in pygame.event.get():
            # Check if Window was asked to close
            if(event.type == pygame.QUIT):
                game_over = True

            # Checking entered keys
            if (event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_LEFT):
                    x_mouvement = -3.5 * 2
                if(event.key == pygame.K_RIGHT):
                    x_mouvement = +3.5 * 2
                if(event.key == pygame.K_UP):
                    y_mouvement = -2
                if(event.key == pygame.K_DOWN):
                    y_mouvement = +3 * 2
                if(event.key == pygame.K_e):
                    egg()
                if(event.key == pygame.K_c):
                    end()
            if event.type == pygame.KEYUP:
                if(event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                    x_mouvement = 0
                if(event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                    y_mouvement = 0

        # Moving THE car and limiting area
        imgrect.move_ip(x_mouvement, y_mouvement)
        if(imgrect.x < 5):
            imgrect.x = 5
        if(imgrect.x > 515):
            imgrect.x = 515
        if(imgrect.y < 5):
            imgrect.y = 5
        if(imgrect.y > 590):
            imgrect.y = 590

        # Moving cars
        imgAmbulanceRect.move_ip(0, car1_speed * 10)
        imgBlackViperRect.move_ip(0, car2_speed * 10)
        imgMiniTruckRect.move_ip(0, car3_speed * 10)
        imgPoliceRect.move_ip(0, car4_speed * 10)

        # Moving background and repeting it
        y_BG += BG_speed * 5
        if(y_BG >= 0):
            y_BG = -170

        # Displaying background
        surface.blit(Background, (x_BG, y_BG))

        #Starting functions
        cars()
        spawnCar(imgrect.x, imgrect.y, imgCar)
        score(current_score)
        pygame.display.update()

        last = 0

        # Checking and choosing column for cars respawns
        if imgAmbulanceRect.y > 800:
            choice = randint(1, 6)
            if(choice == 1 and last != 1):
                imgAmbulanceRect.x = 10
                last = 1
            if(choice == 2 and last != 2):
                imgAmbulanceRect.x = 110
                last = 2
            if(choice == 3 and last != 3):
                imgAmbulanceRect.x = 210
                last = 3
            if(choice == 4 and last != 4):
                imgAmbulanceRect.x = 305
                last = 4
            if(choice == 5 and last != 5):
                imgAmbulanceRect.x = 405
                last = 5
            if(choice == 6 and last != 6):
                imgAmbulanceRect.x = 510
                last = 6
            imgAmbulanceRect.y = -200
            car1_speed = 1

        if imgBlackViperRect.y > 800:
            choice = randint(1, 6)
            if(choice == 1 and last != 1):
                imgBlackViperRect.x = 10
                last = 1
            if(choice == 2 and last != 2):
                imgBlackViperRect.x = 110
                last = 2
            if(choice == 3 and last != 3):
                imgBlackViperRect.x = 210
                last = 3
            if(choice == 4 and last != 4):
                imgBlackViperRect.x = 305
                last = 4
            if(choice == 5 and last != 5):
                imgBlackViperRect.x = 405
                last = 5
            if(choice == 6 and last != 6):
                imgBlackViperRect.x = 510
                last = 6
            imgBlackViperRect.y = -200
            car2_speed = 1.25

        if imgMiniTruckRect.y > 800:
            choice = randint(1, 6)
            if(choice == 1 and last != 1):
                imgMiniTruckRect.x = 10
                last = 1
            if(choice == 2 and last != 2):
                imgMiniTruckRect.x = 110
                last = 2
            if(choice == 3 and last != 3):
                imgMiniTruckRect.x = 210
                last = 3
            if(choice == 4 and last != 4):
                imgMiniTruckRect.x = 305
                last = 4
            if(choice == 5 and last != 5):
                imgMiniTruckRect.x = 405
                last = 5
            if(choice == 6 and last != 6):
                imgMiniTruckRect.x = 510
                last = 6
            imgMiniTruckRect.y = -300
            car3_speed = 1.5

        if imgPoliceRect.y > 800:
            choice = randint(1, 6)
            if(choice == 1 and last != 1):
                imgPoliceRect.x = 10
                last = 1
            if(choice == 2 and last != 2):
                imgPoliceRect.x = 110
                last = 2
            if(choice == 3 and last != 3):
                imgPoliceRect.x = 210
                last = 3
            if(choice == 4 and last != 4):
                imgPoliceRect.x = 305
                last = 4
            if(choice == 5 and last != 5):
                imgPoliceRect.x = 405
                last = 5
            if(choice == 6 and last != 6):
                imgPoliceRect.x = 510
                last = 6
            imgPoliceRect.y = -500
            car4_speed = 1

        # Check if there is a crash and end the game or do nothing is ghost mode is activated (easter egg)
        if(imgrect.colliderect(imgAmbulanceRect) == 1 or imgrect.colliderect(imgBlackViperRect) == 1 or imgrect.colliderect(imgMiniTruckRect) == 1 or imgrect.colliderect(imgPoliceRect) == 1):
            if(g == 0):
                end()

        # Increasing score if THE car passed other cars
        if(imgAmbulanceRect.y - imgrect.y <= 9 and imgAmbulanceRect.y - imgrect.y >= 0 or imgBlackViperRect.y - imgrect.y <= 10 and imgBlackViperRect.y - imgrect.y >= 0 or imgMiniTruckRect.y - imgrect.y <= 10 and imgMiniTruckRect.y - imgrect.y >= 0 or imgPoliceRect.y - imgrect.y <= 9 and imgPoliceRect.y - imgrect.y >= 0):
            current_score = current_score + 1

        # Avoiding car crash by changing speed if there is a collision
        if(imgAmbulanceRect.colliderect(imgBlackViperRect) == 1):
            if(imgAmbulanceRect.y <= imgBlackViperRect.y):
                car1_speed = 0.75
                car2_speed = 1.25
        if(imgAmbulanceRect.colliderect(imgMiniTruckRect) == 1):
            if(imgAmbulanceRect.y <= imgMiniTruckRect.y):
                car1_speed = 0.75
                car3_speed = 1.25
        if(imgAmbulanceRect.colliderect(imgPoliceRect) == 1):
            if(imgAmbulanceRect.y <= imgPoliceRect.y):
                car1_speed = 0.75
                car4_speed = 1.25

        if(imgBlackViperRect.colliderect(imgAmbulanceRect) == 1):
            if(imgBlackViperRect.y <= imgAmbulanceRect.y):
                car2_speed = 0.5
                car1_speed = 1.15
        if(imgBlackViperRect.colliderect(imgMiniTruckRect) == 1):
            if(imgBlackViperRect.y <= imgMiniTruckRect.y):
                car2_speed = 0.5
                car3_speed = 1.15
        if(imgBlackViperRect.colliderect(imgPoliceRect) == 1):
            if(imgBlackViperRect.y <= imgPoliceRect.y):
                car2_speed = 0.5
                car4_speed = 1.15

        if(imgMiniTruckRect.colliderect(imgAmbulanceRect) == 1):
            if(imgMiniTruckRect.y <= imgAmbulanceRect.y):
                car3_speed = 1
                car1_speed = 1.5
        if(imgMiniTruckRect.colliderect(imgBlackViperRect) == 1):
            if(imgMiniTruckRect.y <= imgBlackViperRect.y):
                car3_speed = 1
                car2_speed = 1.5
        if(imgMiniTruckRect.colliderect(imgPoliceRect) == 1):
            if(imgMiniTruckRect.y <= imgPoliceRect.y):
                car3_speed = 1.5
                car4_speed = 1

        if(imgPoliceRect.colliderect(imgAmbulanceRect) == 1):
            if(imgPoliceRect.y <= imgAmbulanceRect.y):
                car4_speed = 0.75
                car1_speed = 1.35
        if(imgPoliceRect.colliderect(imgBlackViperRect) == 1):
            if(imgPoliceRect.y <= imgBlackViperRect.y):
                car4_speed = 0.75
                car2_speed = 1.35
        if(imgPoliceRect.colliderect(imgMiniTruckRect) == 1):
            if(imgPoliceRect.y <= imgPoliceRect.y):
                car4_speed = 1.35
                car3_speed = 0.75

# Start menu function
def menu():
    flag = 0

    # Display the menu picture
    surface.blit(imgMenu, (0, 0))
    pygame.display.update()

    # Checking flag and waiting for input
    while(flag == 0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flag = 1
                    main()
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    quit()

# Easter egg function
def egg():
    # Define secret variables
    cm = "quit()"
    a = None
    global g
    global s
    g = 0

    # Get username from computer
    usr = getpass.getuser()

    # Stop the music
    pygame.mixer.music.stop()

    # Act like a shell
    print("RACER v2.3 by Adrien CL (@SH4FS0c13ty)")
    while(a != cm):
        a = input(usr + "@RACER~$ ")
        if(a == cm):
            pygame.quit()
            quit()
        if(a == "about"):
            print("RACER v2.3 (Python3 and PyGame 1.9.4 on Windows)")
            print("Using Atom (atom.io) editor and Python 3.7")
            print("Author: Adrien CL (@SH4FS0c13ty)")
            print("Facebook: https://github.com/SH4FS0c13ty")
            print("Licensed under MIT License, see 'license.txt'.")
        if(a == "help"):
            print("Available commands:")
            print("about    Show informations about the program and the developer")
            print("edit     Open the RACER.py file with Notepad")
            print("exit     Exit this menu")
            print("ghost    Become a ghost in the game (To stop being a ghost, just return to this menu)")
            print("help     Show the help")
            print("license  Show the license file")
            print("quit()   Quit the game")
            print("score    Enter a number to modify the current score")
        if(a == "edit"):
            # Call an external app (syntax: ["app.exe", "argument1", "argument2", ""]
            call(["npp\\notepad++.exe", "RACER.py"])
        if(a == "exit"):
            menu()
        if(a == "ghost"):
            # Changing flag for ghost mode
            g = 1
            print("Ghost mode activated")
        if(a == "license"):
            # Opening and showing license.txt file content on the console
            f = open('license.txt', 'r')
            file_content = f.read()
            print(file_content)
            f.close()
        if(a == "score"):
            # Changing current score
            global s
            s = int(input("Enter a number:"))
            print("Your current score is:")
            print(s)
            print("Exit this menu and play to see the modified score")

# Start menu function
menu()
