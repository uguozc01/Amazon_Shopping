import os
# absolute path to the directory
currentdir = os.path.dirname(__file__)
os.chdir(currentdir)
from locators import Locators
from data import TestData
from pages import HomePage, SearchResultsPage, ProductDetailsPage, CartPage, SubCartPage

import pytest, time, re
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import InvalidArgumentException

class Test_Base():

    def setup(self):
        ''' setup '''
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(TestData.CHROME_EXECUTABLE_PATH, options=options)
            self.driver.get(TestData.BASE_URL)
        except WebDriverException as e:
            print(e)
        except Exception as e:
            print(e)

    def teardown(self):
        ''' clean up '''
        self.driver.close()
        self.driver.quit()


class Test_Amazon_Search(Test_Base):

    delete = '0 (Delete)'   # this is not a good solution.Find actual Delete element and use it.

    def setup(self):
        super().setup()

    def test_successful_home_page_loading(self):
        ''' Creates an instance of HomePage.
        Then opens browser and navigates to Amazon Home Page '''
        self.homePage=HomePage(self.driver)
        # assert if the title of Home Page contains Amazon.in
        title = self.homePage.driver.title.split(':')[0]
        assert re.search(TestData.HOME_PAGE_TITLE, title)


    def test_user_can_search(self):
        HomePage.setTestData(TestData.SEARCH_TEXT1)
        self.homePage=HomePage(self.driver)
        # search term will be picked up from test data class
        self.homePage.search()
        
        ''' create a new instance of SearchResultsPage class so that will allow 
        newly created object to have access to the browser and perform actions '''
        self.searchResultsPage=SearchResultsPage(self.homePage.driver)
        # assert if the search term is in the title of the Amazon's Search Results
        assert re.search(TestData.SEARCH_LIST[0], self.searchResultsPage.driver.page_source)
        # check if the search term indeed return some results once again
        assert not re.search(TestData.NO_RESULTS_TEXT, self.searchResultsPage.driver.page_source)


    def test_add_item1_save_for_later(self):
        HomePage.setTestData(TestData.SEARCH_TEXT1)
        self.homePage=HomePage(self.driver)
        self.homePage.search()

        self.searchResultsPage=SearchResultsPage(self.homePage.driver)
        # click on the first search result
        self.searchResultsPage.click_search_result()

        # create instance of Product Details Page class
        self.productDetailsPage=ProductDetailsPage(self.searchResultsPage.driver)
        # click on the Add To Cart button
        self.productDetailsPage.click_add_to_cart_button()
        
        # create instance of Sub Cart Page 
        self.subCartPage=SubCartPage(self.productDetailsPage.driver)
        # assert if the sub cart page has indeed loaded
        assert self.subCartPage.is_enabled(Locators.SUB_CART_DIV)
        # assert if the product was added to the cart successfully
        assert self.searchResultsPage.is_visible(Locators.PROCEED_TO_BUY_BUTTON)
        # load the cart page by clicking Cart's hyperlink 
        self.subCartPage.click_cart_link()
        self.subCartPage.click_save_it_for_later()
        assert self.searchResultsPage.is_visible(Locators.CART_IS_EMPTY)


    def test_add_item2_and_delete(self):
        HomePage.setTestData(TestData.SEARCH_TEXT2)
        self.homePage=HomePage(self.driver)
        self.homePage.search()
        
        self.searchResultsPage=SearchResultsPage(self.homePage.driver)
        self.searchResultsPage.click_search_result()
        # self.searchResultsPage.driver.switch_to.window(self.searchResultsPage.driver.window_handles[0])
        
        # create instance of Product Details Page class
        self.productDetailsPage=ProductDetailsPage(self.searchResultsPage.driver)
        # click on the Add To Cart button
        self.productDetailsPage.click_add_to_cart_button()
        # self.productDetailsPage.click_see_buying_options()
        # self.productDetailsPage.click_add_used_one_to_cart()
        
        self.subCartPage=SubCartPage(self.productDetailsPage.driver)
        self.subCartPage.click_cart_link()
        
        self.cartPage=CartPage(self.subCartPage.driver)
        # first check the count of item in the cart
        cartCountBeforeDeletion=int(self.driver.find_element(*Locators.CART_COUNT).text)
        self.cartPage.click_cart()
        self.cartPage.click_quantity(self.delete)
        assert int(self.driver.find_element(*Locators.CART_COUNT).text) < cartCountBeforeDeletion
        assert self.searchResultsPage.is_visible(Locators.CART_IS_EMPTY)


    def test_add_item3_and_save_as_gift(self):
        HomePage.setTestData(TestData.SEARCH_TEXT3)
        self.homePage=HomePage(self.driver)
        self.homePage.search()
        
        self.searchResultsPage=SearchResultsPage(self.homePage.driver)
        # click on the first search result
        self.searchResultsPage.click_search_result()
        
        # create instance of Product Details Page class
        self.productDetailsPage=ProductDetailsPage(self.searchResultsPage.driver)
        # click on the Add To Cart button
        # self.productDetailsPage.click_paperback()
        self.productDetailsPage.click_add_to_cart_button()
        # instantiate an object of Sub Cart Page class
        
        self.subCartPage=SubCartPage(self.productDetailsPage.driver)
        # assert if the sub cart page has indeed loaded
        assert self.subCartPage.is_enabled(Locators.SUB_CART_DIV)
        # assert if the product was added to the cart successfully
        assert self.searchResultsPage.is_visible(Locators.PROCEED_TO_BUY_BUTTON)
        # load the cart page by clicking Cart's hyperlink
        self.subCartPage.click_this_is_a_gift()
        self.subCartPage.click_cart_link()
        cartCountBeforeDeletion=int(self.driver.find_element(*Locators.CART_COUNT).text)

        self.cartPage=CartPage(self.subCartPage.driver)
        self.cartPage.click_quantity(3)
        self.cartPage.click_cart()
        self.driver.implicitly_wait(2)
        self.cartPage.click_quantity(self.delete)  # As "delete" element did not work
        # self.cartPage.delete_item()
        assert int(self.driver.find_element(*Locators.CART_COUNT).text) < cartCountBeforeDeletion
        assert self.searchResultsPage.is_visible(Locators.CART_IS_EMPTY)
