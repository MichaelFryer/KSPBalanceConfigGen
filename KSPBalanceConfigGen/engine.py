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

class Tech:
    def __init__(self,
                 optimalTmr,
                 tmrScaling,
                 maxIsp,
                 minIsp,
                 exponent
                 ):
        self.optimalTmr = float(optimalTmr)
        self.tmrScaling = float(tmrScaling)
        self.maxIsp = float(maxIsp)
        self.minIsp = float(minIsp)
        self.exponent = float(exponent)

    def MaxTmr(self): return self.optimalTmr * self.tmrScaling
    def MinTmr(self): return self.optimalTmr / self.tmrScaling
    def MaxTmrRange(self, maxTmr = None):
        return (self.MaxTmr() if maxTmr == None else maxTmr) - self.optimalTmr
    def MinTmrRange(self, minTmr = None):
        return self.optimalTmr - (self.MinTmr() if minTmr == None else minTmr)
    def IspRange(self): return self.maxIsp - self.minIsp
        
    class TechDerived:
        def __init__(self, tech):
            self.maxTmr = tech.MaxTmr()
            self.minTmr = tech.MinTmr()
            self.maxTmrRange = tech.MaxTmrRange(self.maxTmr)
            self.minTmrRange = tech.MinTmrRange(self.minTmr)
            self.ispRange = tech.IspRange()

    def TmrToIsp(self, tmr, derived = None):

        # Calculate the derived values if none were passed in
        if (derived is None):
            derived = self.TechDerived(self)
            
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

