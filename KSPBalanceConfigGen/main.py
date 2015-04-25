##KSPBalanceConfigGen
##Copyright (C) 2015 Michael Fryer
##
##KSPBalanceConfigGen is free software: you can redistribute it and/or modify
##it under the terms of the GNU General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##KSPBalanceConfigGen is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with KSPBalanceConfigGen.  If not, see <http://www.gnu.org/licenses/>.

import configparser
import engine
import csv
import math

def EngineTechFromParserSection(section):
    return engine.Tech(section['optimalTmr'],
                section['tmrScaling'],
                section['maxIsp'],
                section['minIsp'],
                section['exponent'],
                section['atmosphereMultiplier'])

def EngineConfigFromParserSection(section):
    return engine.Config(techTypes[section['tech']],
                section['baseMass'],
                section['baseSize'],
                section['baseTmrMultiplier'],
                section['sizeMassExponent'],
                section['sizeTmrExponent'])

# Round x to the y most significant digits
def round_to_significant(x, y):
    return round(x, (y-1)-int(math.floor(math.log10(x))))

techFile = 'example_techs.ini'
configFile = 'example_configs.ini'
partFile = 'example_parts.csv'
exportFile = 'd:\example_export.csv'
useCSVExport = True;

# Parse engine tech types
print ("------------------------------")
print ("Loading Engine Tech Types")
print ("------------------------------")
parser = configparser.ConfigParser()
print('Reading: '+techFile)
parser.read(techFile)
techTypes = {}
for section in parser.sections():
    try:
        print("Parsing: "+section)
        techTypes[section] = EngineTechFromParserSection(parser[section])
    except ValueError:
        print (" -- Failed to load engine tech type '"+section+"', "+str(e)+"'")
    except KeyError as e:
        print (" -- Failed to load engine tech type '"+section+"'. Missing Value '"+e.args[0]+"'")
print ("------------------------------")
print("Loaded "+str(len(techTypes))+" engine tech type(s)")
print("")



# Parse engine config types
print ("------------------------------")
print ("Loading Engine Config Types")
print ("------------------------------")

parser = configparser.ConfigParser()
print('Reading: '+configFile)
parser.read(configFile)
configTypes = {}
for section in parser.sections():
    try:
        print("Parsing: "+section)
        configTypes[section] = EngineConfigFromParserSection(parser[section])
    except ValueError as e:
        print (" -- Failed to load engine config type '"+section+"', "+str(e)+"'")
    except KeyError as e:
        print (" -- Failed to load engine config type '"+section+"'. Missing Value '"+e.args[0]+"'")
        
print ("------------------------------")
print ("Loaded "+str(len(configTypes))+" engine config type(s)")
print("")

# Parse individual parts list
print ("------------------------------")
print ("Loading/Balancing Parts")
print ("------------------------------")

engines = {}
print('Opening: '+partFile)
with open(partFile, 'rt', encoding="utf-8") as partsImportFile:
    print('Reading: '+partFile)
    csvReader = csv.reader(partsImportFile, delimiter=',', quotechar='"')
    for row in csvReader:
        try:
            print("Parsing/Balancing: "+str(row[0]))
            engines[str(row[0])] = configTypes[row[2]].EngineFromSize(row[1])
        except ValueError as e:
            print (" -- Failed to load part, "+str(e))
        except IndexError as e:
            print (" -- Failed to load part, missing value")
        except KeyError as e:
            print (" -- Failed to load part, unknown type '"+e.args[0]+"'")
            
print ("------------------------------")
print ("Loaded and balanced "+str(len(engines))+" part(s)")
print("")


print ("------------------------------")
print ("Exporting Parts")
print ("------------------------------")
numPartsWritten = 0

# CSV Export
if useCSVExport:
    print('Exporting to CSV')
    print('Opening: '+exportFile)
    with open(exportFile, 'w', newline='') as partExportFile:
        print('Writing headers')
        csvWriter = csv.writer(partExportFile, delimiter=',',
            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(['Name', 'Mass', 'Thrust', 'Vacuum ISP', 'Atmosphere ISP'])
        for name, eng in engines.items():
            print('Writing part: '+name)
            csvWriter.writerow([name,
                round_to_significant(eng.mass, 2),
                round_to_significant(eng.thrust, 2),
                round_to_significant(eng.vacIsp, 2),
                round_to_significant(eng.atmIsp, 2)])
            numPartsWritten += 1

# Module Manager Config Export
else:
    pass
            
 
print ("------------------------------")
print ("Wrote "+str(len(engines))+" part(s) to "+exportFile)
print("")

        

        
                
                
                                

