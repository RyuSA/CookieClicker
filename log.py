import time
def log(driver, start):
    log = {}
    log["time"] = time.time() - start
    log["Cookies"] = driver.execute_script("return Game.cookiesEarned")
    log["Cps"] = driver.execute_script("return Game.cookiesPs")
    return log