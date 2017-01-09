#!/usr/bin/python
# Add additional metadata to route geoJSON files, by pulling in data from the EMS Cycle Tours spreadsheet.
# Prerequisites:
#   easy_install gspread
#   pip install oauth2client
import os,sys,json, glob, re, gspread 
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('/Users/stevebennett/Dropbox/config/keys/Google API/EMS-cycletours-Python-script-d1495fcb0461.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

print "Login",; gc = gspread.authorize(credentials)
print "Spreadsheet",; spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1QOFfAJy0VHmckNQJWjzHPaP-33N5l4YRY84hYqVzUeo/edit#gid=0")
print "Worksheets",;
calculations=spreadsheet.worksheet("Calculations")
#rawdata=spreadsheet.worksheet("Raw data")
private=spreadsheet.worksheet("Private cycle tours")
print "Header",; header = calculations.row_values(1)
print 'PHeader',; pheader = private.row_values(1)

trips = {}
ptrips = {}
def getColumn(sheet, colName):
    print colName,
    trips[colName] = sheet.col_values(header.index(colName) + 1)[1:]

def getPColumn(colName):
    print colName,
    ptrips[colName] = private.col_values(pheader.index(colName) + 1)[1:]

print 
print "Fetch columns from Calculations sheet: ",
#map(getColumn, ['ID', 'Name', 'Year', 'Participants'])
map(lambda col: getColumn(calculations, col), ['ID', 'Name', 'Year', 'Participants', 'Km', 'Date','Days', 'Alex','Steve','Felix','Ellen','Tom','Dave B','Andrew','Lachie','Matt','Rhonda'])
#map(lambda col: getColumn(calculations, col), ['ID', 'Name', 'Year', 'Participants'])
#print 


# Todo: add properties for each individual's participation (or not), by looping over columns Q(17) to AT(46)
print "Fetch columns from private cycle tours sheet: ",
# Private cycle tours (P3 etc) are looked up in a separate table.
map(getPColumn, ['ID','Name', 'Year', 'Participants'])
print

ptrips['Year'] = map(lambda x: re.search(r"(20\d\d)", x).group(1) if x is not None else -1, ptrips['Year']) 
ptrips['Participants'] = map(lambda x: x.count(",") + 1, ptrips['Participants'])

print "Loaded. Updating files next."

for filename in glob.glob("tmp/*.json"):
    print filename
    m = re.search(r"^tmp\/(P?\d+[a-z]*)-", filename)
    if not m:
        print "%s? We don't have any information about that trip." % filename
        continue

    routefile = open(filename)

    data=json.load(routefile)
    if len(data["features"]) == 0:
        print "Empty JSON file %s, deleting." % filename
        routefile.close
        os.remove(filename)
        continue
  
    routeid = m.group(1)
    
    if routeid[0] != "P":
        attributes = trips
    else:
        attributes = ptrips
    
    index = attributes['ID'].index(routeid)

    props = data["features"][0]["properties"]

    # Copy every property that we looked up, to the geometry properties.
    def setAtt(att):
        props[att] = attributes[att][index]
    map(setAtt, attributes.keys())
    props['Name'] = re.search (r"([^(]+)", props['name']).groups(1)[0].strip()

    # Get rid of a bunch of properties that got inserted during file conversion
    map(lambda prop: props.pop(prop, None), ['src', 'elevationChartUrlMap', 'link1_href', 'link1_text', 'link1_type', 'link2_href', 'link2_text', 'link2_type', 'cmt', 'type', 'desc', 'number'])
    print props

    routefile.close
    routefile = open(filename,"wb")
    json.dump(data, routefile)
    routefile.close
