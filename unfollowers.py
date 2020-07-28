import time
from selenium import webdriver

class IGbot:
    # Logging in
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(4)
        self.driver.find_element_by_xpath("//button[@type='button']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        time.sleep(3)

    def _get_names(self):
        time.sleep(2)
        scrollbox = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", scrollbox)

        #comapare the scrollheight to the start
        #to determine the end of the scrollbox
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            time.sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scrollbox)
        #names of my following
        links = scrollbox.find_elements_by_tag_name('a')
        ignames = [name.text for name in links if name.text != '']
        #close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button")\
            .click()
        return ignames

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}')]".format(self.username))\
            .click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}/following/')]".format(self.username))\
            .click()
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}/followers/')]".format(self.username))\
            .click()
        followers = self._get_names()
        #put the names of everyone thats not following me into a list
        not_following_back = [user for user in following if user not in followers]
        #print whoever is not following back line by line
        print(*not_following_back, sep = "\n")




mybot = IGbot('username', 'password')
mybot.get_unfollowers()
