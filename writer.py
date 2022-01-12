import rdflib
from rdflib.namespace import RDF, RDFS, XSD

prefixBase = 'http://oxfordsemantic.tech/transactions/'
mainPrefix = prefixBase + 'entities#'
propPrefix = prefixBase + 'properties#'
typePrefix = prefixBase + 'classes#'

mainNS = rdflib.Namespace(mainPrefix)
propNS = rdflib.Namespace(propPrefix)
typeNS = rdflib.Namespace(typePrefix)

def generateNode(type, id):
    return mainNS[type + '_' + id]

def generateClass(name):
    return typeNS[name]

def generateProperty(name):
    return propNS[name]

def generateBoolean(letter):
    return rdflib.Literal(letter == 'Y')

def writeGraph(outputPath, fileFormat, parties, transactions):
    g = rdflib.Graph()

    g.bind('', mainNS)
    g.bind('prop', propNS)
    g.bind('type', typeNS)
    g.bind('rdf', RDF)
    g.bind('rdfs', RDFS)
    g.bind('xsd', XSD)

    partyClass = generateClass('Party')

    internalProperty = generateProperty('isInternal')
    fullNameProperty = generateProperty('hasFullName')
    exitedProperty = generateProperty('isExited')
    suspiciousProperty = generateProperty('isSuspicious')

    for party in parties:
        partyIri = generateNode('party', party['id'])
        g.add((partyIri, RDF.type, partyClass))

        internalBoolean = generateBoolean(party['internal'])
        g.add((partyIri, internalProperty, internalBoolean))

        if party['firstName'] != None:
            fullName = rdflib.Literal(party['firstName'] + ' ' + party['lastName'])
            g.add((partyIri, fullNameProperty, fullName))
            g.add((partyIri, RDFS.label, fullName))

        exitedBoolean = generateBoolean(party['exited'])
        g.add((partyIri, exitedProperty, exitedBoolean))

        suspiciousBoolean = generateBoolean(party['isSuspicious'])
        g.add((partyIri, suspiciousProperty, suspiciousBoolean))

    transactionClass = generateClass('Transaction')
    originatorProperty = generateProperty('hasOriginator')
    beneficiaryProperty = generateProperty('hasBeneficiary')
    amountProperty = generateProperty('hasAmount')
    dateProperty = generateProperty('hasDate')

    for transaction in transactions:
        transactionIri = generateNode('transaction', transaction['id'])
        g.add((transactionIri, RDF.type, transactionClass))

        originatorIri = generateNode('party', transaction['originator']['id'])
        g.add((transactionIri, originatorProperty, originatorIri))

        beneficiaryIri = generateNode('party', transaction['beneficiary']['id'])
        g.add((transactionIri, beneficiaryProperty, beneficiaryIri))

        amount = rdflib.Literal(transaction['amount'], datatype=XSD.decimal)
        g.add((transactionIri, amountProperty, amount))

        date = rdflib.Literal(transaction['date'], datatype=XSD.dateTime)
        g.add((transactionIri, dateProperty, date))

    g.serialize(destination=outputPath, format=fileFormat)