from selenium.webdriver.common.by import By

class Locators():

    #  All necessary ocators for Home Page 
    SEARCH_CATEGORY=(By.ID, 'searchDropdownBox')
    SEARCH_TEXT=(By.ID, 'twotabsearchtextbox')
    SEARCH_SUBMIT=(By.XPATH,'//*[@id="nav-search-submit-button"]')
    
    # Search Result Page Image
    SEARCH_RESULT_LINK=(By.XPATH, '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div[2]/div/span/div/div/span/a/div/img')

    # Search Details Page
    ADD_TO_CART_BUTTON=(By.ID, 'add-to-cart-button')
    ADD_USED_ONE_TO_CART=(By.XPATH, '//*[@id="a-autoid-2"]/span/input')

    # Cart Page
    REMOVE_FROM_CART=(By.XPATH,"//div[contains(@class,'a-row sc-action-links')]//span[contains(@class,'sc-action-delete')]")
    SAVE_FOR_LATER =(By.XPATH,"//div[contains(@class,'a-row sc-action-links')]//span[contains(@class,'sc-action-save-for-later')]")
    HOVER_QTY_ICON=(By.XPATH,'//*[@id="a-autoid-0"]/span/i')
    QUANTITY=(By.XPATH,f"//select[contains(@class,'sc-update-quantity-select')]")
    CART_COUNT=(By.ID,'nav-cart-count')
    PROCEED_TO_CHECKOUT_BUTTON=(By.NAME,"proceedToCheckout")
    IS_TO_BE_GIFT_WRAPPPED=(By.XPATH,'//*[@id="gutterCartViewForm"]/div/div/div[2]/div')

    # Sub Cart 
    SUB_CART_DIV=(By.XPATH, '//*[@id="hlb-subcart"]') 
    CART_COUNT=(By.ID,"nav-cart-count")
    CART_LINK=(By.ID,"nav-cart")  # The one with shopping cart symbol
    PROCEED_TO_BUY_BUTTON=(By.ID,"hlb-ptc-btn-native")
    CART_IS_EMPTY=(By.XPATH, '//*[@id="sc-active-cart"]/div/div/div/h1')
    ORDER_AS_A_GIFT=(By.XPATH,'//*[@id="huc-v2-order-row-mark-gift"]/div/label/input')

    # Product Details
    SEE_BUYING_OPTIONS=(By.XPATH, '//*[@id="a-autoid-2-announce"]')
    PAPERBACK=(By.XPATH,'//*[@id="mediaTab_heading_1"]/a')
