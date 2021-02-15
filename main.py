import sys
from skeleton import Repository


args = sys.argv                             #using args
repo = Repository()                         # create and initialize the repository
repo.createTables()                         # create tables
repo.initializeDatabase(args[1])            # initialize tables due to 'config.txt' file
repo.handleShipments(args[2])               # handling all the shipments from 'order.txt' file
repo.writeSummaryOnFile(args[3])            # create the summary









