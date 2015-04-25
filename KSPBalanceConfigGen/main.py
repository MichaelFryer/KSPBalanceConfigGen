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

# Parse engine tech types
print ("------------------------------")
print ("Loading Engine Tech Types")
print ("------------------------------")
parser = configparser.ConfigParser()
parser.read('example_techs.ini')
techTypes = {}
for section in parser.sections():
    try:
        print("Loading: "+section)
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
parser.read('example_configs.ini')
configTypes = {}
for section in parser.sections():
    try:
        print("Loading: "+section)
        configTypes[section] = EngineConfigFromParserSection(parser[section])
    except ValueError as e:
        print ("Failed to load engine config type '"+section+"', "+str(e)+"'")
    except KeyError as e:
        print ("Failed to load engine config type '"+section+"'. Missing Value '"+e.args[0]+"'")
        
print ("------------------------------")
print ("Loaded "+str(len(configTypes))+" engine config type(s)")
print("")


for cfgKey in configTypes:
    for s in [0.625, 1.25, 2.5, 3.75]:
        eng = configTypes[cfgKey].EngineFromSize(s)

        print (
            ", "+str(eng.mass)+
            ", "+str(eng.thrust)+
            ", "+str(eng.vacIsp)+
            ", "+str(eng.atmIsp))

        
                
                
                                

