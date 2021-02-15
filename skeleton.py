import sqlite3
import os

#DTO
from typing import List

#DTO
class vaccine:


    def __init__(self, id, date, supplier, quantity):
        self._id = id
        self._date = date
        self._supplier = supplier
        self._quantity = quantity

    def getId(self):
        return self._id
    def getDate(self):
        return self._date
    def getSupplier(self):
        return self._supplier
    def getQuantity(self):
        return self._quantity

    def setId(self, id):
        self._id = id
    def setDate(self, date):
        self._date = date
    def setSupplier(self, supplier):
        self._supplier = supplier
    def setQuantity(self, quantity):
        self._quantity = quantity
class supplier:

    def __init__(self, id, name, logistic):
        self._id = id
        self._name = name
        self._logistic = logistic

    def getId(self):
        return self._id
    def getName(self):
        return self._name
    def getLogistic(self):
        return self._logistic
class clinic:

    def __init__(self, id, location, demand, logistic):
        self._id = id
        self._location = location
        self._demand = demand
        self._logistic = logistic

    def getId(self):
        return self._id
    def getLocation(self):
        return self._location
    def getDemand(self):
        return self._demand
    def getLogistic(self):
        return self._logistic
class logistic:

    def __init__(self, id, name, count_sent, count_received):
        self._id = id
        self._name = name
        self._count_sent = count_sent
        self._count_received = count_received

    def getId(self):
        return self._id
    def getName(self):
        return self._name
    def getCount_sent(self):
        return self._count_sent
    def getCount_received(self):
        return self._count_received


#DAO
class Vaccines(object):

    def __init__(self, conn):
        self._conn = conn
    def insert(self, vaccine):
        """
        :type vaccine: vaccine
        """
        s = """ INSERT INTO vaccines (id, date, supplier, quantity) VALUES ({a}, {b}, {c}, {d})""".format(a = vaccine.getId(), b  = "'" + vaccine.getDate()+ "'", c = vaccine.getSupplier(), d = vaccine.getQuantity())
        self._conn.executescript(s)
    def getOldest(self):                    #return the oldest vaccine
        vals = self.getOldestAssist()
        return vaccine(vals[0], vals[1], vals[2], vals[3])
    def getOldestAssist(self):
        s = "SELECT id, MIN(date), supplier, quantity FROM vaccines"
        val = self._conn.execute(s)
        return list(val.fetchone())
    def updateQuantity(self, vaccine):
        s = "UPDATE vaccines SET quantity = {a} WHERE id = {b} ".format(a = vaccine.getQuantity(), b = vaccine.getId())
        self._conn.executescript(s)
    def removeById(self, vaccine):
        s = "DELETE FROM vaccines WHERE id = {a}".format(a = vaccine.getId())
        self._conn.executescript(s)
    def getNewId(self):
        s = "SELECT MAX(id) FROM vaccines"
        tmp = self._conn.execute(s)     #get biggest id
        return int(*tmp.fetchone()) + 1
    def getTotalQuantity(self):
        s = "SELECT SUM(quantity) FROM vaccines"
        quantity = self._conn.execute(s)
        return int(*quantity.fetchone())
class Suppliers:

    def __init__(self, conn):
        self._conn = conn
    def insert(self, supplier):
        """
        :type supplier: supplier
        """
        s = """ INSERT INTO suppliers (id, name, logistic) VALUES ({a}, {b}, {c})""".format(a = supplier.getId(), b = "'" + supplier.getName() +"'", c =  supplier.getLogistic())
        self._conn.executescript(s)

    def getIdByName(self, name):
        s = "SELECT id FROM suppliers WHERE name = {a}".format(a="'" + name + "'")
        id = self._conn.execute(s)
        return str(*id.fetchone())

    def getLogisticByName(self, name):
        s = "SELECT logistic FROM suppliers WHERE name = {a}".format(a="'" + name + "'")
        id = self._conn.execute(s)
        return str(*id.fetchone())
class Clinics:

    def __init__(self, conn):
        self._conn = conn
    def insert(self, clinic):
        """
        :type clinic: clinic
        """
        s = """ INSERT INTO clinics (id, location, demand, logistic) VALUES ({a}, {b}, {c}, {d})""".format(a = clinic.getId(), b = "'" + clinic.getLocation() + "'", c = clinic.getDemand(), d = clinic.getLogistic())
        self._conn.executescript(s)

    def updateDemandByLocation(self, location, amount):
        oldDemand = self.getDemandByLocation(location)
        s = "UPDATE clinics SET demand = {a} WHERE location = {b}".format(a= oldDemand - amount, b = "'" + location + "'")
        self._conn.executescript(s)

    def getDemandByLocation(self, location):
        s = "SELECT demand FROM clinics WHERE location = {a}".format(a = "'" + location + "'")
        demand = self._conn.execute(s)
        # print (str(*demand.fetchone()))
        return int(*demand.fetchone())


    def getLogisticIdByLocation(self, location):
        s = "SELECT logistic FROM clinics WHERE location = {a}".format(a = "'" + location + "'")
        tmp = self._conn.execute(s)
        return int(*tmp.fetchone())
    def getTotalDemand(self):
        s = "SELECT SUM(demand) FROM clinics"
        demand = self._conn.execute(s)
        return int(*demand.fetchone())
class Logistics:

    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic1):
        """
        :type logistic1: logistic
        """

        s = "INSERT INTO logistics VALUES ({a}, {b}, {c}, {d})".format(a = int(logistic1.getId()),b = "'" + logistic1.getName() +"'" , c = int(logistic1.getCount_sent()), d = int(logistic1.getCount_received()))
        self._conn.executescript(s)

    def updateCount_SentById(self, logisticId, amount):
        oldCount_Sent = self.getCount_sentById(logisticId)
        s = "UPDATE logistics SET count_sent = {a} WHERE id = {b}".format(a = oldCount_Sent + amount, b = logisticId)
        self._conn.executescript(s)
    def updateCount_ReceivedById(self, logisticId, amount):
        s = "UPDATE logistics SET count_received = count_received + {a} WHERE id = {b}".format(a = amount, b = logisticId)
        self._conn.executescript(s)


    def getCount_sentById(self, ID):
        s = "SELECT count_sent FROM logistics WHERE id = {a}".format(a = ID)
        tmp = self._conn.execute(s)
        return int(*tmp.fetchone())



    def getTotalCountSent(self):
        s = "SELECT SUM(count_sent) FROM logistics"
        count_sent = self._conn.execute(s)
        return int(*count_sent.fetchone())

    def getTotalCountReceived(self):
        s = "SELECT SUM(count_received) FROM logistics"
        count_received = self._conn.execute(s)
        return int(*count_received.fetchone())



#repository
class Repository:

    def __init__(self):
        self._conn = sqlite3.connect('database')
        self.vaccines = Vaccines(self._conn)
        self.suppliers = Suppliers(self._conn)
        self.clinics = Clinics(self._conn)
        self.logistics = Logistics(self._conn)
        self.summary = ""
    def close(self):
        self._conn.commit()
        self._conn.close()
    def createTables(self):
        if os.path.isfile("database"):
            self.close()
            os.remove("database")
            self.__init__()
        self._conn.executescript(""" CREATE TABLE vaccines (
                        id              INTEGER     PRIMARY KEY,
                        date            DATE        NOT NULL,
                        supplier        INTEGER     REFERENCES supplier(id), 
                        quantity        INTEGER     NOT NULL
                        );

                        CREATE TABLE suppliers (
                        id              INTEGER     PRIMARY KEY,
                        name            STRING      NOT NULL,
                        logistic        INTEGER     REFERENCES logistic(id) 
                        );

                        CREATE TABLE clinics (
                        id              INTEGER     PRIMARY KEY,
                        location        STRING      NOT NULL,
                        demand          INTEGER     NOT NULL,
                        logistic        INTEGER     REFERENCES logistic(id)
                        );

                        CREATE TABLE logistics (
                        id              INTEGER     PRIMARY KEY,
                        name            TEXT      NOT NULL,
                        count_sent      INTEGER     NOT NULL,
                        count_received  INTEGER     NOT NULL
                        ); 
                    """)
    def initializeDatabase(self, fileName):
        """
        :type adress: String
        """
        file = open(fileName, "r")  # open file
        lines = file.readlines()  # read all lines
        nums: List[str] = lines[0].split(",")
        numOfVaccines = (int(nums[0]))
        numOfSupplier = (int(nums[1]))
        numOfClinics = (int(nums[2]))
        numOfLogistic = (int(nums[3]))


        ind = 1 + numOfVaccines + numOfSupplier + numOfClinics
        # create logistic table
        for i in range(0, numOfLogistic):
            curr = lines[ind].split(",")
            curr = logistic(int(curr[0]), curr[1], int(curr[2]), int(curr[3]))
            self.logistics.insert(curr)
            ind += 1

        ind = 1 + numOfVaccines
        # create supplier table
        for i in range(0, numOfSupplier):
            curr = lines[ind].split(",")
            curr = supplier(curr[0], curr[1], curr[2])
            self.suppliers.insert(curr)
            ind += 1

        ind = 1
        # create vaccine table
        for i in range(0, numOfVaccines):
            curr = lines[ind].split(",")
            curr = vaccine(curr[0], curr[1], curr[2], curr[3])
            self.vaccines.insert(curr)
            ind += 1

        ind = 1 + numOfVaccines + numOfSupplier
        # create clinics table
        for i in range(0, numOfClinics):
            curr = lines[ind].split(",")
            curr = clinic(curr[0], curr[1], curr[2], curr[3])
            self.clinics.insert(curr)
            ind += 1

        file.close()
    def handleShipments(self, fileName):
        file = open(fileName, "r")  # open file
        lines = file.readlines()  # read all lines
        for i in range (0, len(lines)):
            shipment = lines[i]
            shipment = shipment.split(",")
            if len(shipment) == 2:
                self.sendShipment(shipment)
            else :
                self.receiveShipment(shipment)

            self.updateSummary()

        self._conn.commit()
        file.close()

    def sendShipment(self, shipment):           #shipment = [location, amount] --> [Tel-Aviv , 50]
        amount = int(shipment[1])

        #update vaccine table
        while amount > 0:
            currVaccine = self.vaccines.getOldest()

            if currVaccine.getQuantity() - amount > 0:
                tmp = currVaccine.getQuantity()

                currVaccine.setQuantity(currVaccine.getQuantity() - amount)
                amount = amount - tmp
                self.vaccines.updateQuantity(currVaccine)
            else:
                remove = currVaccine.getQuantity()
                self.vaccines.removeById(currVaccine)
                amount = amount - remove

        location = shipment[0]
        amount = int(shipment[1])

        #update clinic table
        self.clinics.updateDemandByLocation(location, amount)

        #get id from the logistic company
        logisticId = self.clinics.getLogisticIdByLocation(location)

        #update count_sent
        self.logistics.updateCount_SentById(logisticId, amount)
    def receiveShipment(self, shipment):

        #update vaccine table
        newId = self.vaccines.getNewId()
        supplierId = self.suppliers.getIdByName(shipment[0])
        currVaccine = vaccine(newId, shipment[2], supplierId, shipment[1])
        self.vaccines.insert(currVaccine)

        #update count_received
        newId = self.suppliers.getLogisticByName(shipment[0])
        self.logistics.updateCount_ReceivedById(newId, shipment[1])
    def updateSummary(self):
        totalDemand = str(self.clinics.getTotalDemand())
        count_sent = str(self.logistics.getTotalCountSent())
        count_received = str(self.logistics.getTotalCountReceived())
        totalInventory = str(self.vaccines.getTotalQuantity())
        tmp = totalInventory +"," + totalDemand  + "," + count_received + "," + count_sent
        self.summary += tmp + "\n"
    def writeSummaryOnFile(self, fileName):
        file = open(fileName, "w")  # open file
        file.write(self.summary)
        file.close()




