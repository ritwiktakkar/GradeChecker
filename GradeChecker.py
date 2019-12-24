import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# Improting Image class from PIL module
from PIL import Image
import time


def make_chrome_headless():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument("--log-level=3")  # fatal
    headless_driver = webdriver.Chrome(executable_path=config.path_to_chromedriver, chrome_options=options)
    return headless_driver


def get_grades():
    # set a driver: headless or display
    # uncomment below to make chrome headless
    driver = make_chrome_headless()
    # uncomment below to display browser
    # webdriver.Chrome(executable_path=config.path_to_chromedriver)
    # log-in
    print("Logging in...")
    driver.get(config.link_to_login)
    driver.find_element_by_name("userid").send_keys(config.MYSLICE_USERNAME)
    driver.find_element_by_name("pwd").send_keys(config.MYSLICE_PASSWORD)
    driver.find_element_by_name("Submit").click()
    driver.get(config.link_to_grades)
    # navigate to fall 2019 grades
    print("Login successful!\nChecking grades...")
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    driver.find_element_by_css_selector(config.css_selector_fall_2019).click()
    driver.find_element_by_xpath(config.xpath_continue_button).click()
    print("Getting a screenshot of your grades...")
    time.sleep(10)
    driver.execute_script("window.scrollTo(0, 150)")
    grades_png = driver.get_screenshot_as_file("fall2019grades_uncropped.png")
    driver.quit()
    return grades_png


def crop_image():
    uncropped_image = Image.open("fall2019grades_uncropped.png")
    print("Adding a screenshot of your grades to the project directory...")
    cropped_image = uncropped_image.crop((0, 125, 600, 525))
    cropped_image.save("fall2019grades.png")
    print("Done!")


def main():
    get_grades()
    crop_image()


if __name__ == "__main__":
    main()
