import os
import re
import sys
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# # Warning download does not currently work with HEADLESS MODE
# if len(sys.argv) != 3:
#     print("Usage: python scrap_freemidi_org.py <genre> <Headless State 1/0>")
#     sys.exit(1)

CHROMEDRIVER_PATH = './scrap_midi/chromedriver'
# HEADLESS = int(sys.argv[2])
WINDOW_SIZE = "800,600"
DEBUG = True  # Debug mode

# Make sure the paths for the chromedriver and chrome is correct
if sys.platform == "linux" or sys.platform == "linux2":
    # linux
    CHROME_PATH = '/usr/bin/google-chrome'
elif sys.platform == "darwin":
    print("os")
    # OSX
    CHROME_PATH = ('/Applications/Google\ Chrome.app/Contents/MacOS/chromedriver')
elif sys.platform == "win32":
    # Windows
    CHROME_PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# Check for HEADLESS state for the chrome driver
# and add window and executable options for chrome
# chrome_options = Options()
# # if HEADLESS:
# #     chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
# chrome_options.binary_location = CHROME_PATH
#
#
# # Initiate the webdriver
# # driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
# #                           options=chrome_options)
#
# driver = webdriver.Chrome(options=chrome_options)
# # Initiate the webdriver
# # driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)

options = webdriver.ChromeOptions()
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
chrome_driver_binary = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)


def click_and_download_song(song):
    try:
        time.sleep(5)
        continue_link = driver.find_elements_by_link_text(".mid")
        print("continue_link",continue_link.text)
        continue_link.click()
    except Exception as e:
        print(e)

    #
    # print("inside clicker", continue_link.text)
    # print("inside")

# def find_artists(genre):
def find_artists():

    # Value Hardcoded as the entire script will be specific to freemidi.org
    # driver.get("https://freemidi.org/genre-" + genre)
    driver.get("http://www1.cpdl.org/wiki/index.php/Giovanni_Pierluigi_da_Palestrina")

    # print(f"driver.title = {driver.title}") if (DEBUG) else print('', end='')

    # div containing artists
    # continue_link = driver.find_element_by_link_text('Continue')
    entire_page = driver.find_elements_by_xpath("/html/body/div[3]/div[3]/div[4]/div")


    l_songs = []
    for elem in entire_page:
        # table_index = 1
        table_index = 8

        tb_index = 2
        link_index = 1
        while table_index in range(1, 10):
            while tb_index in range(1, 4):
                while True:
                    time.sleep(0.7)
                    try:
                        # xp = "/html/body/div[3]/div[3]/div[4]/div/table[1]/tbody/tr/td[1]/ul/li[1]/a"
                        # print(f"Enter song,{table_index},{tb_index},{link_index} ")

                        song = elem.find_element_by_xpath(
                            f"//table[{table_index}]/tbody/tr/td[{tb_index}]/ul/li[{link_index}]/a")
                        print(song.text, end='\n' + ('#' * 10))

                        time.sleep(0.7)
                        song.click()
                        link_index += 1

                        # click_and_download_song(song)
                        try:
                            time.sleep(0.7)
                            elems = driver.find_elements_by_xpath("//a[@href]")
                            for elem in elems:
                                href_txt = elem.get_attribute("href")

                                if href_txt.find('.mid') != -1 or href_txt.find('.midi') != -1:
                                    print("must be mid", elem.get_attribute("href"))
                                    elem.click()


                        except Exception as e:
                            print(e)
                        time.sleep(1.7)
                        driver.back()

                        entire_page = driver.find_elements_by_xpath("/html/body/div[3]/div[3]/div[4]/div")
                        elem = entire_page[0]
                        # song = elem.find_element_by_xpath(
                        #     f"//table[{table_index}]/tbody/tr/td[{tb_index}]/ul/li[{link_index}]/a")
                        # l_songs.append(song)


                    except Exception as e:
                        print(e)
                        print(f"exception,{table_index},{tb_index},{link_index} ")
                        if table_index > 9:
                            table_index = 11
                            tb_index = 5
                            break
                        else:
                            if tb_index > 3:
                                table_index += 1
                                tb_index = 1
                                link_index = 1
                            else:
                                tb_index += 1
                                link_index = 1


        return



    mainContent = driver.find_element_by_link_text("/wiki/index.php")
    print("information about mainContent.\ntype:",type(mainContent),"\n length:",len(mainContent),"\ncontent:",mainContent)
    # List of artists
    mainContentList = driver.find_element_by_link_text(".mid")
    # /wiki/index.php

    # making sure element not found erros are ignored
    # any errors will be logged in the error_log file
    os.makedirs("logs", exist_ok=True)
    with open('./logs/error_log', 'a') as elog:
        try:
            artist_link_count = len(mainContent)
            list_index = 405
            while list_index < artist_link_count:
                time.sleep(0.4)
                # div containing artists
                try:
                    # mainContent = driver.find_element_by_link_text("/wiki/index.php")
                    # midfile = driver.find_element_by_link_text(".mid")
                    mainContent.find_element_by_link_text(".mid")[list_index].click()
                    # artist_name = mainContent.find_elements_by_xpath(
                    #     ".//div/a[2]")[list_index].text
                except:
                    print("midi file DNE")
                    list_indexex += 1

                # goto artist page

        except:
            print("exception at line 95")

        #         # div containing artist songs
        #         mainContentSong = driver.find_element_by_xpath(
        #             "//div[@id='mainContent']")
        #         songContentList = mainContentSong.find_elements_by_xpath(
        #             ".//div[1]/div[@class='artist-container']/div[1]/div/div[@class='artist-song-cell']/span/a")
        #
        #         song_link_count = len(songContentList)
        #         current_song_page = 2  # Due to the indexing of the elements, it starts with 2
        #         song_list_index = 0
        #         while song_list_index < song_link_count:
        #             try:
        #                 # for song_list_index in range(initial_Start, song_link_count):
        #                 # div containing artist songs
        #                 mainContentSong = driver.find_element_by_xpath(
        #                     "//div[@id='mainContent']")
        #                 time.sleep(0.7)  # To make sure page has loaded
        #                 # goto song download page
        #                 song_download_link = mainContentSong.find_elements_by_xpath(
        #                     ".//div[1]/div[@class='artist-container']/div[1]/div/div[@class='artist-song-cell']")[song_list_index]
        #             except:
        #                 print(f"Song List index {song_list_index} out of range on page title {driver.title}")
        #                 song_list_index += 1
        #                 continue
        #             song_download_link = song_download_link.find_element_by_xpath(
        #                 ".//span/a")
        #
        #             with open('./logs/downloaded_songs.txt', 'a') as f:
        #                 log = "artist_list_index = " + str(list_index) + ", artist = " + \
        #                     str(artist_name) + ", song_list_index = " +\
        #                     str(song_list_index) + ', ' + \
        #                     song_download_link.text
        #                 print(log.encode("utf-8"), file=f)
        #                 print(log)
        #
        #             # goto download page
        #             song_download_link.click()
        #             time.sleep(0.4)
        #             try:
        #                 midi_download_link_str = "//*[@id='downloadmidi']"
        #                 midi_download_link = ui.WebDriverWait(driver, 10).until(
        #                     EC.element_to_be_clickable((By.XPATH, midi_download_link_str)))
        #
        #             except:
        #                 print("Download link absent")
        #                 song_list_index += 1
        #                 driver.back()
        #                 continue
        #             time.sleep(0.5)
        #             midi_download_link.click()
        #             song_list_index += 1
        #
        #             driver.back()  # Go back to song list page for artist
        #
        #             # If we are at the last song, check if another song page exists
        #             if song_list_index == (song_link_count - 1):
        #                 page_lists = driver.find_elements_by_xpath(
        #                     "//div[@id='mainContent']/div[1]/div[2]/div[2]/nav/ul/li")
        #                 page_count = len(page_lists)
        #                 if page_count >= 4 and current_song_page < (page_count-1):  # if page_count == 3 then only one page exists
        #                     current_song_page += 1
        #                     next_page_string = "//div[@id='mainContent']/div[1]/div[2]/div[2]/nav/ul/li[" \
        #                         + str(current_song_page) + ']/a'
        #                     next_page = ui.WebDriverWait(driver, 50).until(
        #                         EC.element_to_be_clickable((By.XPATH, next_page_string)))
        #
        #                     # go to the next page
        #                     next_page.click()
        #                     # div containing artist songs
        #                     mainContentSong = driver.find_element_by_xpath(
        #                         "//div[@id='mainContent']")
        #                     songContentList = mainContentSong.find_elements_by_xpath(
        #                         ".//div[1]/div[@class='artist-container']/div[1]/div/div[@class='artist-song-cell']/span/a")
        #
        #                     song_link_count = len(songContentList)
        #                     song_list_index = 0
        #
        #         driver.back()
        #         list_index += 1
        # except Exception as ex:
        #     template = "Unix Time: " + \
        #         str(time.time()) + \
        #         ": An exception of type {0} occurred. Arguments:\n{1!r}"
        #     traceback.print_exc()
        #     message = template.format(type(ex).__name__, ex.args)
        #     elog.write((message + '\n'))



def main():
    # Get the music genre
    # genre = sys.argv[1]

    find_artists()
    driver.close()


if __name__ == "__main__":
    main()
