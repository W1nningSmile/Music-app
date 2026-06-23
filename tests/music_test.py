import pygame


pygame.mixer.init()  # Initialize the mixer module.
sound1 = pygame.mixer.Sound('songs/Album/Sheer_Heart_Attack/Killer_Queen.mp3')  # Load a sound.

while True:
    inpt = input('Press enter to play the sound: ')
    sound1.play()  # Play the sound.
    print(i)
    print('Playing sound')