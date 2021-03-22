from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions


def find_element(driver, by, value):
    ignored_exceptions = (
        NoSuchElementException,
        StaleElementReferenceException,)
    return WebDriverWait(
        driver, 10, ignored_exceptions=ignored_exceptions).until(
        expected_conditions.presence_of_element_located((by, value)))


def element_exists(driver, by, value):
    try:
        find_element(driver, by, value)
    except TimeoutException:
        return False
    return True


class Page(object):

    def __init__(self, home, driver=None):
        self.home_address = home
        self.driver = driver if driver else webdriver.Chrome()

    def navigate_home(self):
        self.driver.get(self.home_address)


class CarsDotComPage(Page):
    def __init__(self, driver=None):
        super().__init__("https://www.cars.com/", driver)

    class Filters:

        def __init__(self, driver):
            self._driver = driver

        @classmethod
        def used_car(cls, driver):
            selector = Select(
                cls(driver).__get_filter_element(
                    "//div/select[@aria-label='Select a stock type']"))
            selector.select_by_value("28881")  # Used car value

        @classmethod
        def model_pilot(cls, driver):
            selector = Select(
                cls(driver).__get_filter_element(
                    "//*[@id='ae-main-content']/section[2]/div/form/div/div[3]/div/select"))
            selector.select_by_value("21729")  # Model:Pilot

        @classmethod
        def make_honda(cls, driver):
            selector = Select(
                cls(driver).__get_filter_element(
                    "//*[@id='ae-main-content']/section[2]/div/form/div/div[2]/div/select"))
            selector.select_by_value("20017")  # Make:Honda

        @classmethod
        def max_price_50000(cls, driver):
            # would make a namedtuple with available prices to pass in here rather than having 50000 specific func.
            selector = Select(
                cls(driver).__get_filter_element(
                    "//div/select[@aria-label='Select a maximum price']"))
            selector.select_by_value("50000")  # Max Price 50000

        @classmethod
        def distance_100_mile_radius(cls, driver):
            # again would make named tuple to pass in for ease of use by mapping accepted values to dot notation
            selector = Select(
                cls(driver).__get_filter_element(
                    "//div/select[@aria-label='Select a maximum distance']"))
            selector.select_by_value("100")  # 100 miles

        @classmethod
        def distance_zip(cls, driver, zip_code):
            selector = cls(driver).__get_filter_element(
                    "//div/input[@aria-label='Enter a Zip Code']")
            selector.send_keys(zip_code)

        @classmethod
        def search_with_filter(cls, driver):
            cls(driver).__get_filter_element(
                         '//*[@id="ae-main-content"]/section[2]/div/form/div/div[6]/input').click()

        def __get_filter_element(self, xpath):
            return find_element(self._driver, By.XPATH, xpath)


class SearchResultsPage(Page):

    def __init__(self, driver):
        super().__init__(
            "https://www.cars.com/for-sale/searchresults.action/?mdId=21729&mkId=20017&prMx=50000&rd=100&searchSource=QUICK_FORM&stkTypId=28881&zc=92870",
            driver
        )

    class FilterRefinements:

        new_car = '//*[@id="stkTypId"]/ul/li[2]'
        trim_8pass_touring = '//*[@id="trId"]/ul/li[9]'

    def refine_search_for_new_cars(self):
        find_element(self.driver, By.XPATH, self.FilterRefinements.new_car).click()

    def refine_search_8pass_touring_trim(self):
        find_element(self.driver, By.XPATH, self.FilterRefinements.trim_8pass_touring).click()

    def select_listing(self, list_index):
        """
        clicks the specific listing based on the list_index
        :param list_index: the index of the listing to select. i.e. 2 will select the second listing on the page.
        :type list_index: int

        """
        xpath = f'//*[@id="srp-listing-rows-container"]/div/a[@data-position="{list_index}"]'
        find_element(self.driver, By.XPATH, xpath).click()

    def find_filter_labels(self):
        filter_labels = list()
        index = 1
        while True:
            xpath = f'//*[@id="ae-main-content"]/div[4]/cars-filters/div[1]/div[1]/header/div/ul/li[{index}]/label'
            if element_exists(self.driver, By.XPATH, xpath):
                breadcrumb_label_text = find_element(self.driver, By.XPATH, xpath).text
                filter_labels.append(breadcrumb_label_text)
                index += 1
            else:
                break
        return filter_labels


class VehicleDetailPage(Page):

    def __init__(self, driver):
        super().__init__("https://www.cars.com/vehicledetail/detail/824695418/overview/", driver)

    @property
    def title(self):
        return self.driver.title

    @property
    def check_availability_button(self):
        return find_element(
            self.driver, By.XPATH,
            '//*[@id="vdpe-leadform"]/div[2]/cars-vdp-serverside-lead-form/div/native-lead-form/form/div[8]/button')

    def input_contact_info(self, first_name, last_name, email):
        first_name_field = find_element(
            self.driver, By.XPATH,
            '//*[@id="vdpe-leadform"]/div[2]/cars-vdp-serverside-lead-form/div/native-lead-form/form/div[1]/div[1]/input')
        first_name_field.send_keys(first_name)

        last_name_field = find_element(
            self.driver, By.XPATH,
            '//*[@id="vdpe-leadform"]/div[2]/cars-vdp-serverside-lead-form/div/native-lead-form/form/div[1]/div[2]/input')
        last_name_field.send_keys(last_name)

        email_name_field = find_element(
            self.driver, By.XPATH,
            '//*[@id="vdpe-leadform"]/div[2]/cars-vdp-serverside-lead-form/div/native-lead-form/form/div[1]/div[3]/input')
        email_name_field.send_keys(email)

    @property
    def payment_calculator(self):
        return find_element(
            self.driver, By.XPATH,
            '//*[@id="calculator-top"]/div/div[1]')


def test_search_for_car():
    """
    Tests the ability to perform and refine a search, and click a resulting listing
    """
    driver = webdriver.Chrome()
    driver.maximize_window()

    cars_page = CarsDotComPage(driver)
    cars_page.navigate_home()
    cars_page.Filters.used_car(driver)
    cars_page.Filters.make_honda(driver)
    cars_page.Filters.model_pilot(driver)
    cars_page.Filters.max_price_50000(driver)
    cars_page.Filters.distance_100_mile_radius(driver)
    cars_page.Filters.distance_zip(driver, "60008")
    cars_page.Filters.search_with_filter(driver)

    search_results_page = SearchResultsPage(driver)
    filter_labels = search_results_page.find_filter_labels()

    assert "Maximum Price: $50,000" in filter_labels
    assert "Honda" in filter_labels
    assert "Pilot" in filter_labels
    assert "Used" in filter_labels

    search_results_page.refine_search_for_new_cars()  # Needs to run script or refresh page to refresh breadcrumbs
    filter_labels = search_results_page.find_filter_labels()
    assert "New" in filter_labels
    assert "Used" not in filter_labels

    search_results_page.refine_search_8pass_touring_trim()  # Needs to run script or refresh page to refresh breadcrumbs
    filter_labels = search_results_page.find_filter_labels()
    assert "Touring 8-Passenger" in filter_labels

    search_results_page.select_listing(2)
    vehicle_details_page = VehicleDetailPage(driver)
    assert all(item in vehicle_details_page.title for item in ["Honda Pilot", "8-Passenger", "For Sale"])
    assert vehicle_details_page.check_availability_button.is_displayed()

    vehicle_details_page.input_contact_info("Car", "Owner", "carowner@yahoo.com")
    actions = ActionChains(driver)
    actions.move_to_element(vehicle_details_page.payment_calculator).perform()
    driver.save_screenshot("payment_calculator.png")
