from requests import Session
import json
import csv
from calendar import monthrange

speciesToLookFor = ['Danaus plexippus', 'Hyles lineata', 'Zerene cesonia', 'Papilio multicaudata', 'Agraulis vanillae', 'Papilio cresphontes', 'Strymon melinus', 'Vanessa cardui', 'Hylephila phyleus', 'Danaus gilippus']

def getTaxaIdsFor(speciesList):
    '''
        This is a function that will return a list of the obsrvation count from 
        iNaturalist of the species in the given list speciesList.

        in: list of species
        out: dictionary of observation count of the given species.
    '''

    idsOfSpecies = {}

    session = Session()

    for species in speciesToLookFor:
        response = session.get('http://api.inaturalist.org/v1/taxa/autocomplete?q=' + species)
        jsonVar = json.loads(response.text)
    
        for elemInResults in jsonVar['results']:
            if elemInResults['name'] == species:
                idsOfSpecies[species] = elemInResults['id']
    return idsOfSpecies

def getObservationCountFor(idList, fromMonth, toMonth, year):
    speciesObservationCounts = {}
    session = Session()
    count = 0

    for speciesName, id in idList.items():
        observationCount = []
        for i in range(fromMonth, toMonth + 1):
            firstDayOfMonth = str(year) + '-' + str(i) + '-01'
            lastDayOfMonth = str(year) + '-' + str(i) + '-' + str(monthrange(int(year), i)[1])
            url = 'http://api.inaturalist.org/v1/observations?taxon_id=' + str(id) + '&d1=' + str(firstDayOfMonth) + '&d2=' + str(lastDayOfMonth)
            response = session.get(url)
            jsonVar = json.loads(response.text)
            observationCount.append(jsonVar["total_results"])
        speciesObservationCounts[speciesName] = observationCount
    
    return speciesObservationCounts
            

def outputAsCsv(dictionary):
    speciesNamePlusCounts = []
    months = [["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]]

    for key, value in dictionary.items():
        countsRow = []
        countsRow.append(key)

        for elem in value:
            countsRow.append(elem)
        speciesNamePlusCounts.append(countsRow)
    
    data = speciesNamePlusCounts

    with open("./species_count.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(months)
        writer.writerows(data)

def main(): 
    idsList = getTaxaIdsFor(speciesToLookFor)
    speciesMonthlyObservations = getObservationCountFor(idsList, 1, 12, '2016')
    outputAsCsv(speciesMonthlyObservations)

if __name__ == '__main__':
    main()