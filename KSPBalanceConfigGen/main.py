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
import sys

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

# Parse command line
if len(sys.argv) < 5:
    print ('Too few arguments')
    print ('Usage: main.py techFile configFile partFile exportFile [templateFile]')
    sys.exit(0)

techFilePath = sys.argv[1]
configFilePath =  sys.argv[2]
partFilePath =  sys.argv[3]
exportFilePath =  sys.argv[4]

useCSVExport = True;
if len(sys.argv) > 5:
    templateFilePath =  sys.argv[5]
    useCSVExport = False;

# Parse engine tech types
print ("------------------------------")
print ("Loading Engine Tech Types")
print ("------------------------------")
parser = configparser.ConfigParser()
print('Reading: '+techFilePath)
parser.read(techFilePath)
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
print('Reading: '+configFilePath)
parser.read(configFilePath)
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

engines = []
print('Opening: '+partFilePath)
with open(partFilePath, 'rt', encoding="utf-8") as partsImportFile:
    print('Reading: '+partFilePath)
    csvReader = csv.reader(partsImportFile, delimiter=',', quotechar='"')
    for row in csvReader:
        try:
            print("Parsing/Balancing: "+str(row[0]))
            eng = configTypes[row[2]].EngineFromSize(row[1])
            eng.module = str(row[3])
            eng.name = str(row[0])
            if (len(row) > 4):
                eng.index = int(row[4])
            else:
                eng.index = int(0)
            engines.append(eng)
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
    print('Opening: '+exportFilePath)
    with open(exportFilePath, 'w', newline='') as partExportFile:
        print('Writing headers')
        csvWriter = csv.writer(partExportFile, delimiter=',',
            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(['Name', 'Mass', 'Thrust', 'Vacuum ISP', 'Atmosphere ISP'])
        for eng in engines:
            print('Writing part: '+eng.name)
            csvWriter.writerow([eng.name,
                round_to_significant(eng.mass, 3),
                round_to_significant(eng.thrust, 3),
                round_to_significant(eng.vacIsp, 3),
                round_to_significant(eng.atmIsp, 3)])
            numPartsWritten += 1

# Module Manager Config Export
else:
    print('Exporting to Module Manager cfg')
    print('Reading Template File: '+templateFilePath)
    with open(templateFilePath, 'r') as templateFile:
        template = templateFile.read()
    print('Opening: '+exportFilePath)
    with open(exportFilePath, 'w', newline='') as partExportFile:
        print('Erasing file')
        partExportFile.truncate()
        for eng in engines:
            print('Writing part: '+eng.name)
            mmcfg = template
            mmcfg = mmcfg.replace('%NAME%', eng.name)
            mmcfg = mmcfg.replace('%MASS%', str(round_to_significant(eng.mass,3)))
            mmcfg = mmcfg.replace('%MODULE%', eng.module)
            if (eng.index != 0):
                mmcfg = mmcfg.replace('%INDEX%', ','+str(eng.index))
            else:
                mmcfg = mmcfg.replace('%INDEX%', '')
            mmcfg = mmcfg.replace('%THRUST%', str(round_to_significant(eng.thrust,3)))
            mmcfg = mmcfg.replace('%VACISP%', str(round_to_significant(eng.vacIsp,3)))
            mmcfg = mmcfg.replace('%ATMISP%', str(round_to_significant(eng.atmIsp,3)))
            partExportFile.write(mmcfg)
            numPartsWritten += 1
            
 
print ("------------------------------")
print ("Wrote "+str(numPartsWritten)+" part(s) to "+exportFilePath)
print("")

        

        
                
                
                                

