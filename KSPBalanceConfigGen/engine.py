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

    # Helper class to cache derived values
    class TechDerived:
        def __init__(self, tech):
            self.maxTmr = tech.MaxTmr()
            self.minTmr = tech.MinTmr()
            self.maxTmrRange = tech.MaxTmrRange(self.maxTmr)
            self.minTmrRange = tech.MinTmrRange(self.minTmr)
            self.ispRange = tech.IspRange()

    # Given a TMR, calculate the vacuum ISP
    def TmrToVacIsp(self, tmr, derived = None):

        # Calculate the derived values if none were passed in
        if (derived is None):
            derived = self.TechDerived(self)
        assert type(derived) is TechDerived, "derived is not an "+__name__+".Tech.TechDerived"
            
        # Find the linear distance between optimal and min or max represented 
        # as a percent in the range 0 to 1
        if (tmr < self.optimalTmr):
            ispPenalty = (self.optimalTmr-tmr)/derived.minTmrRange
        else:
            ispPenalty = (tmr-self.optimalTmr)/derived.maxTmrRange

        # Apply the exponential scaling
        ispPenalty **= self.exponent

        # Convert from a percent penalty to an actual penalty based on the ISP range
        ispPenalty *= derived.ispRange

        # Finally calculate the actual ISP by subtracting the penalty from the maximum
        return self.maxIsp - ispPenalty

    # Given a TMR, calculate the atmospheric ISP
    def TmrToAtmIsp(self, derived = None):
        return self.VacIspToAtmIsp(TmrToVacIsp(derived))

    # Convert a vacuum ISP to an atmosphere one
    def VacIspToAtmIsp (self, vacIsp):
        return vacIsp * self.atmosphereMultiplier

    # Convert a atmospheric ISP to a vacuum one
    def AtmIspToVacIsp (self, atmIsp):
        return atmIsp / self.atmosphereMultiplier

# An engine config type which defines a relationship between size (diameter in meters)
# and mass/TMR .
# The TMR (thrust to mass ratio) is given as a value between 0 and 2 where 1.0 is the base
# TMR of the related tech type, 0 is the minimum and 2 is the maximum, values outside this
# are truncated.
class Config:
    def __init__(self,
                 tech,
                 baseMass,
                 baseSize,
                 baseTmrMutliplier,
                 sizeMassExponent,
                 sizeTmrExponent
                 ):
        self.tech = str(tech)
        self.baseMass = float(baseMass)
        self.baseSize = float(baseSize)
        self.baseTmrMutliplier = float(baseTmrMutliplier)
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

    # Calculate the actual TMR for a given size and tech
    def TmrFromSize(self, size, tech):
        assert type(tech) is Tech, "tech is not a "+__name__+".tech"
        tmrMultiplier = self.TmrMultiplierFromSize(size)
        if (tmrMultiplier > 1):
            return ((tmrMultiplier-1)*tech.MaxTmrRange())+tech.optimalTmr
        else:
            return ((tmrMultiplier-1)*tech.MinTmrRange())+tech.optimalTmr
    
    
        

    
