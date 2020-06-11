def login(driver, target_url):
    driver.get(target_url)
    driver.find_element_by_id("login_id").send_keys("triose")
    driver.find_element_by_id("password").send_keys("triose123")
    driver.find_element_by_tag_name('button').click()
