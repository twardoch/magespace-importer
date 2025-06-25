#!/usr/bin/env python3

import logging
import time
from pathlib import Path

import fire
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
from undetected_chromedriver import Chrome

# Configure logging
logging.basicConfig(level=logging.INFO, format="\n>> %(message)s")
logger = logging.getLogger(__name__)


class MagespaceModelImporter:
    """A class to import models from a list of URLs into mage.space."""

    def __init__(
        self,
        models_path: Path | str | None = None,
        driver_path: Path | str | None = None,
        url_import: str | None = None,
    ):
        """
        Initialize the MagespaceModelImporter class.

        Args:
            models_path (Path | str | None): Path to the file containing model URLs.
            driver_path (Path | str | None): Path to the ChromeDriver executable.
            url_import (str | None): URL to the model import page.
        """
        self.models_path = (
            Path(models_path).resolve()
            if models_path
            else Path(Path.cwd() / "magespace.txt").resolve()
        )
        if not self.models_path.exists():
            logger.error(
                f"You must have the file\n{self.models_path}\nthat contains a newline-delimited list of model URLs."
            )
            return
        self.driver = self.initialize_driver(driver_path)
        self.url_import = url_import or "https://www.mage.space/models/import"
        self.run()

    def initialize_driver(self, driver_path: Path | str | None) -> webdriver.Chrome:
        """
        Initialize and return a Chrome WebDriver.

        Args:
            driver_path (Path | str | None): Path to the ChromeDriver executable.

        Returns:
            webdriver.Chrome: An instance of Chrome WebDriver.
        """
        if driver_path:
            driver = Chrome(executable_path=str(Path(driver_path).resolve()))
        else:
            driver = Chrome()
        return driver

    def is_logged_in(self) -> bool:
        """
        Check if the user is logged in.

        Returns:
            bool: True if logged in, False otherwise.
        """
        logger.info(
            "Please log into mage.space using your account, then click here and press Enter"
        )
        input(">>> Waiting for Enter...")

        try:
            self.driver.find_element(
                By.CSS_SELECTOR,
                "iframe[src*='https://www.mage.space/__/auth/iframe']",
            )
            logger.info("Logged in successfully.")
            return True
        except NoSuchElementException:
            logger.error("Error logging in")
            return False

    def open_new_tab(self, url: str) -> None:
        """
        Open a new tab in the browser with the specified URL.

        Args:
            url (str): URL to open in the new tab.
        """
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(url)

    def wait_for_element(self, selector: str, timeout: int = 10) -> WebElement:
        """
        Wait for an element to be visible and return it.

        Args:
            selector (str): CSS selector of the element to wait for.
            timeout (int): Time in seconds to wait for the element.

        Returns:
            WebElement: The found web element.
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def process_model_url(self, model_url: str) -> None:
        """
        Process a single model URL by opening a tab and entering the URL.

        Args:
            model_url (str): The model URL to process.
        """
        self.open_new_tab(self.url_import)
        time.sleep(1)
        model_url_field = self.wait_for_element("input[type='text']")
        model_url_field.clear()
        model_url_field.send_keys(model_url)
        time.sleep(1)
        # Additional steps to process the model URL...

    def read_model_urls(self) -> list[str]:
        """
        Read model URLs from a file.

        Returns:
            list[str]: A list of model URLs.
        """
        return self.models_path.read_text().splitlines()

    def process_urls(self, model_urls: list[str]) -> list[str]:
        """
        Process multiple model URLs.

        Args:
            model_urls (list[str]): A list of model URLs to process.

        Returns:
            list[str]: A list of URLs that failed to process.
        """
        error_urls = []
        for model_url in tqdm(
            model_urls,
            total=len(model_urls),
            desc="Opening tabs for models",
            unit="url",
        ):
            try:
                self.process_model_url(model_url)
            except Exception as e:
                logger.error(f"Error processing URL {model_url}: {e}")
                error_urls.append(model_url)
        return error_urls

    def wait_for_manual_processing(self) -> None:
        """
        Wait for the user to manually process and close tabs.
        """
        logger.info("Please finish each import and close each tab!")
        initial_tab_count = len(self.driver.window_handles)
        previous_tab_count = initial_tab_count

        with tqdm(total=initial_tab_count, desc="Closed tabs", unit="tab") as pbar:
            while len(self.driver.window_handles) > 0:
                current_tab_count = len(self.driver.window_handles)
                tabs_closed = previous_tab_count - current_tab_count
                if tabs_closed > 0:
                    pbar.update(tabs_closed)
                    previous_tab_count = current_tab_count
                time.sleep(1)

    def run(self) -> None:
        """
        Run the model importing process.
        """
        self.driver.get(self.url_import)
        if self.is_logged_in():
            model_urls = self.read_model_urls()
            error_urls = self.process_urls(model_urls)
            if error_urls:
                logger.error(f"Failed URLs: {error_urls}")

            self.wait_for_manual_processing()
            logger.info("Finished processing all models!")
        self.driver.quit()


def import_models_to_magespace(
    models_path: Path | str | None = None,
    driver_path: Path | str | None = None,
    url_import: str | None = None,
) -> None:
    """
    Helps importing models from a list of URLs into https://mage.space/

    `magespace_importer` is a Python-based tool designed to simplify importing models from a list of URLs into https://mage.space/

    It opens each URL in a new browser tab, and lets you perform the model import there. After you've imported a model, close the tab. To finish processing, close all browser tabs.

    ## Installation

    Ensure Python 3.10 or higher is installed on your system. You can then install the package using pip:

    ```bash
    python3 -m pip install --upgrade git+https://github.com/twardoch/magespace-importer
    ```

    ## Usage

    Prepare a text file containing a list of URLs to models you want to import, one URL per line, and save it as `magespace.txt` in your current folder.

    For example, for models from CivitAI, you can use URLs like:

    ```text
    https://civitai.com/api/download/models/243915?type=Model&format=SafeTensor&size=pruned&fp=fp16
    https://civitai.com/api/download/models/163063?type=Model&format=SafeTensor
    ```

    > Note: If a model page on CivitAI has one Download button, you can use the CivitAI model page URL. But if the model page has a download dropdown, you must click it and copy the download URL (typically SafeTensors).

    Then, use the tool in command line with optional arguments:

    ```bash
    magespace_importer
    ```

    ### Optional Arguments

    - `--models_path`: Path to the text file containing model URLs (one URL per line), defaults to `magespace.txt` in the current folder.
    - `--driver_path`: Optional path to the ChromeDriver executable.
    - `--url_import`: Custom URL for the model import page, defaults to `https://www.mage.space/models/import`.

    Example:

    ```bash
    magespace_importer --models_path /path/to/magespace.txt
    ```

    or if `magespace.txt` is in the current folder:

    ```bash
    magespace_importer
    ```

    """
    MagespaceModelImporter(models_path, driver_path, url_import)


def cli():
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire(import_models_to_magespace)


if __name__ == "__main__":
    cli()
