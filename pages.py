import os, time
# absolute path to the directory
currentdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(currentdir)
from locators import Locators
from data import TestData

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC


class BasePage():
    """Parent class for all the pages
    Contains all common actions and elements available to all pages"""

    def __init__(self, driver):
        self.driver=driver

    '''performs click on web element'''
    def click(self, by_locator):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located(by_locator))
        element.click()

    '''performs submit'''
    def submit_button(self, by_locator):
        wait = WebDriverWait(self.driver, 10)
        submit_element = wait.until(EC.visibility_of_element_located(by_locator))
        submit_element.submit()

    ''' shopping cart can be reachable from basepage'''
    def click_shopping_cart(self, by_locator):
        wait = WebDriverWait(self.driver, 10)
        cart = wait.until(EC.visibility_of_element_located(by_locator))
        cart.click()

    '''Compare web element text to text we pass in'''
    def assert_element_text(self, by_locator, element_text):
        wait = WebDriverWait(self.driver, 10)
        web_element=wait.until(EC.visibility_of_element_located(by_locator))
        assert web_element.text == element_text

    '''put text into the web element '''
    def enter_text(self, by_locator, text):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.visibility_of_element_located(by_locator)).send_keys(text)

    '''checks if the web element is enabled or not, returns web element if enabled'''
    def is_enabled(self, by_locator):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.visibility_of_element_located(by_locator))

    '''this function checks if the web element is visible or not and returns true or false'''
    def is_visible(self,by_locator):
        wait = WebDriverWait(self.driver, 10)
        element=wait.until(EC.visibility_of_element_located(by_locator))
        return bool(element)

    'hovering function'
    def hover_to(self, by_locator):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located(by_locator))
        AC(self.driver).move_to_element(element).click().perform()

    def select_qty(self, by_locator):
        drv = self.driver
        drv.implicitly_wait(2)
        # selection = wait.until(EC.visibility_of_element_located(by_locator))
        return Select(drv.find_element_by_xpath(by_locator))
 

class HomePage(BasePage):
    """Home Page of Amazon"""

    test_data = ''

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(TestData.BASE_URL)

    def search(self):
        self.driver.find_element(*Locators.SEARCH_TEXT).clear()
        self.enter_text(Locators.SEARCH_TEXT, self.test_data)
        self.click(Locators.SEARCH_SUBMIT)

    '''I am using this classmethod to change search text outside the class 
    so that I can test with different search texts'''
    @classmethod    
    def setTestData(cls, test_data):
        cls.test_data = test_data


class SearchResultsPage(BasePage):
    """Search Results"""
    def __init__(self, driver):
        super().__init__(driver)        

    def click_search_result(self):
        self.click(Locators.SEARCH_RESULT_LINK)

    
class ProductDetailsPage(BasePage):
    ''' Details of search results when clicked on product image'''
    def __init__(self,driver):
        super().__init__(driver)

    ''' Paperback Part '''

    def click_paperback(self):
        self.click(Locators.PAPERBACK)

    def click_add_to_cart_button(self):
        self.click(Locators.ADD_TO_CART_BUTTON)
    
    def click_see_buying_options(self):
        self.click(Locators.SEE_BUYING_OPTIONS)
    
    def click_add_used_one_to_cart(self):
        self.click(Locators.ADD_USED_ONE_TO_CART)

    def buy_now(self):
        pass

    ''' Kindle Part '''

    def click_kindle(self):
        pass

    def buy_with_one_click(self):
        pass

    def send_a_free_sample(self):
        pass

    def give_as_a_gift(self):
        pass


class SubCartPage(BasePage):

    def __init__(self,driver):
        super().__init__(driver)

    def click_cart_link(self):
        self.click(Locators.CART_LINK)

    def click_proceed_to_checkout(self):
        pass

    def click_this_is_a_gift(self):
        self.click(Locators.ORDER_AS_A_GIFT)

    def click_save_it_for_later(self):
        self.click(Locators.SAVE_FOR_LATER)


class CartPage(BasePage):

    def __init__(self,driver):
        super().__init__(driver)
    
    def delete_item(self):

        cartCount=int(self.driver.find_element(*Locators.CART_COUNT).text)
        if cartCount < 1:
            print("Cart is empty")
            exit()

        self.click(Locators.REMOVE_FROM_CART)
    
    def click_save_for_later(self):
        self.click(Locators.SAVE_FOR_LATER)

    def hover_quantity_icon(self):
        self.hover_to(Locators.HOVER_QTY_ICON)

    def click_quantity(self, opt):
        element = self.select_qty(Locators.QUANTITY[1])
        element.select_by_visible_text(str(opt))

    def click_cart(self):
        self.click_shopping_cart(Locators.CART_LINK)

    def click_proceed_to_checkout_button(self):
        self.click(Locators.PROCEED_TO_CHECKOUT_BUTTON)