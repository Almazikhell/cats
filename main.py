import time
from sprite import *
import pygame as pg


def dialogue_mode(sprite, text):
    screen.blit(space, (0, 0))
    screen.blit(sprite.image, sprite.rect)
    sprite.update()
    print(text_number)
    text1 = f1.render(text[text_number], True, pg.Color("white"))
    screen.blit(text1, (275, 400))
    if text_number < len(text) - 1:
        text2 = f1.render(text[text_number + 1], True, pg.Color("white"))
        screen.blit(text2, (275, 420))


pg.init()
pg.mixer.init()

size = (800, 600)
screen = pg.display.set_mode(size)
pg.display.set_caption("Космические коты")

FPS = 120
clock = pg.time.Clock()

ali = Alien()
cap = Captain()
starship = Starship()
heart = pg.image.load("heart.png")
heart = pg.transform.scale(heart, (40, 40))

is_running = True
mode = "start_scene"

meteorites = pg.sprite.Group()
mice = pg.sprite.Group()
lasers = pg.sprite.Group()
space = pg.image.load("bg.png")
start_text = ["Мы засекли сигнал с планеты Мур.",
              "",
              "Наши друзья, инопланетные коты,",
              "нуждаются в помощи.",
              "Космические мыши хотят съесть их луну,",
              "потому что она похожа на сыр.",
              "Как долго наш народ страдал от них, ",
              "теперь и муряне в беде...",
              "Мы должны помочь им.",
              "Вылетаем прямо сейчас.",
              "Спасибо, что починил звездолёт, штурман. ",
              "Наконец-то функция автопилота работает.",
              "Поехали!"]

alien_text = ["СПАСИТЕ! МЫ ЕЛЕ ДЕРЖИМСЯ!",
              "",
              "Мыши уже начали грызть луну...",
              "Скоро куски луны будут падать на нас.",
              "Спасите муриан!", ]

final_text = ["Огромное вам спасибо,",
              "друзья с планеты Мяу!",
              "Как вас называть? Мяуанцы? Мяуриане?",
              "В любом случае, ",
              "теперь наша планета спасена!",
              "Мы хотим отблагодарить вас.",
              "Капитан Василий и его штурман получают",
              "орден SKYSMART.",
              "А также несколько бутылок нашей",
              "лучшей валерьянки.",
              ""]

text_number = 0
f1 = pg.font.Font("font.otf", 25)
start_time = 0

hearts = 5
pg.mixer.music.load("ST.wav")
pg.mixer.music.play()
pg.mixer_music.set_volume(0.02)

laser_sfx = pg.mixer.Sound("laser.wav")
win = pg.mixer.Sound("win_msc.wav")
while is_running:

    # СОБЫТИЯ
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False
        if event.type == pg.KEYDOWN:

            if mode == "start_scene":
                text_number += 2
                if len(start_text) < text_number:
                    start_time = time.time()
                    text_number = 0
                    mode = "meteorites"
            if mode == "final_scene":

                text_number += 2
                if len(final_text) < text_number:
                    start_time = time.time()
                    text_number = 0
                    is_running = False
            if mode == "alien_scene":
                text_number += 2
                if len(alien_text) < text_number:
                    start_time = time.time()
                    text_number = 0
                    mode = "moon"
                    starship.switch_mode()
            if mode == "moon":
                if event.key == pg.K_SPACE:
                    laser_sfx.play()
                    lasers.add(Laser((starship.rect.x+50, starship.rect.y)))


    # ОБНОВЛЕНИЯ
    if mode == "start_scene":
        dialogue_mode(cap, start_text)

    if mode == "meteorites":
        if time.time() - start_time > 10:
            mode = "alien_scene"

        screen.blit(space, (0, 0))
        if random.randint(0, 100) == 1:
            meteorites.add(Meteorite())

        starship.update()

        screen.blit(starship.image, starship.rect)
        meteorites.update()
        meteorites.draw(screen)

        hits = pg.sprite.spritecollide(starship, meteorites, True)

        for hit in hits:
            hearts -= 1
            if hearts == 0:
                is_running = False

        for i in range(hearts):
            screen.blit(heart, (i*30,0))

    if mode == "alien_scene":
        dialogue_mode(ali, alien_text)

    if mode == "moon":
        if time.time() - start_time > 10:
            mode = "final_scene"

            win.play()

        screen.blit(space, (0, 0))

        if random.randint(0, 100) == 1:
            mice.add(Mouse_starship())

        starship.update()
        mice.update()
        lasers.update()

        screen.blit(starship.image,starship.rect)
        mice.draw(screen)
        lasers.draw(screen)

        hits = pg.sprite.spritecollide(starship, mice, True)

        for hit in hits:
            hearts -= 1
            if hearts == 0:
                is_running = False

        for i in range(hearts):
            screen.blit(heart, (i * 30, 0))

        pg.sprite.groupcollide(lasers, mice, True, True)







    if mode == "final_scene":
        dialogue_mode(ali, final_text)

    pg.display.flip()
    clock.tick(FPS)
