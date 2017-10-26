
class Building(object):
    product = "product"

    def __init__(self, name ,id , driver):
        self.id = id
        self.productid = "product" + str(id)
        self.name = name
        self.execute_ThisBuilding = "Game.ObjectsById[" + str(id) + "]"
        self.Cps = driver.execute_script("return " + self.execute_ThisBuilding + ".storedCps;")
        self.price =  driver.execute_script("return " + self.execute_ThisBuilding + ".price;")
        # self.owned =  driver.execute_script("return " + self.execute_ThisBuilding + ".bought;")
        self.Cps_per_price = self.Cps / self.price
        # self.is_active = False
        # self.is_active = "enabled" in driver.find_element_by_id(self.productid).get_attribute("class")

    def Buy(self, bought_number, driver):
        # クリックさせるよりも高速
        driver.execute_script(self.execute_ThisBuilding + ".buy(" + str(bought_number) + ");")
        self.Cps = driver.execute_script("return " + self.execute_ThisBuilding + ".storedCps;")
        self.price =  driver.execute_script("return " + self.execute_ThisBuilding + ".price;")
        # self.owned =  driver.execute_script("return " + self.execute_ThisBuilding + ".bought;")
        self.Cps_per_price = self.Cps / self.price
    
    def Sell(self, sold_number, driver):
        driver.execute_script(self.execute_ThisBuilding + ".sell(" + str(bought_number) + ");")
        self.Cps = driver.execute_script("return " + self.execute_ThisBuilding + ".storedCps;")
        self.price =  driver.execute_script("return " + self.execute_ThisBuilding + ".price;")
        # self.owned =  driver.execute_script("return " + self.execute_ThisBuilding + ".bought;")
        self.Cps_per_price = self.Cps / self.price
    
    def is_active(self, driver):
        return "enabled" in driver.find_element_by_id(self.productid).get_attribute("class")

    def is_unlocked(self, driver):
        return "unlocked" in driver.find_element_by_id(self.productid).get_attribute("class")

    def Update(self, driver):
        self.Cps = driver.execute_script("return " + self.execute_ThisBuilding + ".storedCps;")
        self.price =  driver.execute_script("return " + self.execute_ThisBuilding + ".price;")
        # self.owned =  driver.execute_script("return " + self.execute_ThisBuilding + ".bought;")
        self.Cps_per_price = self.Cps / self.price
        # self.is_active = "enabled" in driver.find_element_by_id(self.productid).get_attribute("class")
