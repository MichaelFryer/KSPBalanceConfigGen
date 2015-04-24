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


# An engine tech type which defines a relationship between thrust to mass ratio (TMR) and ISP
class Tech:
    def __init__(self,
                 optimalTmr,
                 tmrScaling,
                 maxIsp,
                 minIsp,
                 exponent,
                 atmosphereMultiplier
                 ):
        self.optimalTmr = float(optimalTmr)
        self.tmrScaling = float(tmrScaling)
        self.maxIsp = float(maxIsp)
        self.minIsp = float(minIsp)
        self.exponent = float(exponent)
        self.atmosphereMultiplier = float(atmosphereMultiplier)

    # Functions that derive useful values from only the class instance variables
    def MaxTmr(self): return self.optimalTmr * self.tmrScaling
    def MinTmr(self): return self.optimalTmr / self.tmrScaling
    def MaxTmrRange(self, maxTmr = None):
        return (self.MaxTmr() if maxTmr == None else maxTmr) - self.optimalTmr
    def MinTmrRange(self, minTmr = None):
        return self.optimalTmr - (self.MinTmr() if minTmr == None else minTmr)
    def IspRange(self): return self.maxIsp - self.minIsp

    # Given a TMR, calculate the vacuum ISP
    def TmrToVacIsp(self, tmr):
            
        # Find the linear distance between optimal and min or max represented 
        # as a percent in the range 0 to 1
        if (tmr < self.optimalTmr):
            ispPenalty = (self.optimalTmr-tmr)/self.MinTmrRange()
        else:
            ispPenalty = (tmr-self.optimalTmr)/self.MaxTmrRange()

        # Apply the exponential scaling
        ispPenalty **= self.exponent

        # Convert from a percent penalty to an actual penalty based on the ISP range
        ispPenalty *= self.IspRange()

        # Finally calculate the actual ISP by subtracting the penalty from the maximum
        return self.maxIsp - ispPenalty

    # Given a TMR, calculate the atmospheric ISP
    def TmrToAtmIsp(self):
        return self.VacIspToAtmIsp(TmrToVacIsp(derived))

    # Convert a vacuum ISP to an atmosphere one
    def VacIspToAtmIsp (self, vacIsp):
        return vacIsp * self.atmosphereMultiplier

    # Convert a atmospheric ISP to a vacuum one
    def AtmIspToVacIsp (self, atmIsp):
        return atmIsp / self.atmosphereMultiplier

    # Get the TMR using a TmrMultiplier
    def TmrFromTmrMultiplier(self, tmrMultiplier):
        # Clamp the value to valid range
        max(min(tmrMultiplier, 2.0), 0.0)
        if (tmrMultiplier > 1):
            return ((tmrMultiplier-1)*self.MaxTmrRange())+self.optimalTmr
        else:
            return ((tmrMultiplier-1)*self.MinTmrRange())+self.optimalTmr
        

# An engine config type which defines a relationship between size (diameter in meters)
# and mass/tmrMultiplier .
class Config:
    def __init__(self,
                 tech,
                 baseMass,
                 baseSize,
                 baseTmrMultiplier,
                 sizeMassExponent,
                 sizeTmrExponent
                 ):
        self.tech = str(tech)
        self.baseMass = float(baseMass)
        self.baseSize = float(baseSize)
        self.baseTmrMultiplier = float(baseTmrMultiplier)
        self.sizeMassExponent = float(sizeMassExponent)
        self.sizeTmrExponent = float(sizeTmrExponent)

    # Calculate the mass for a given size
    def MassFromSize(self, size):
        return self.baseMass*((size/self.baseSize)**self.sizeMassExponent)

    # Calculate the tmrMultiplier for a given size
    def TmrMultiplierFromSize(self, size):
        tmrMultiplier = self.baseTmrMutliplier*((size/self.baseSize)**self.sizeTmrExponent)
        # Clamp the value to valid range
        return max(min(tmrMultiplier, 2.0), 0.0)

class Engine
    def __init__(self,
                 name,
                 tmr,
                 mass,
                 vacIsp,
                 atmIsp,
                 ):
        self.name = str(name)
        self.mass = (float)mass
        self.thrust = mass * (float)tmr
        self.vacIsp = (float)vacIsp
        self.atmIsp = (float)atmIsp
