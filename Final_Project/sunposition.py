import math
import numpy

## AUXILIAR FUNCTIONS ##

def day_number(month, day):
  #list of months#
  months= ["January", "February", "March", "April", "May", "June", "July", "" ] 
  if type(month)== str:

  return "shit"

def frac_hours(hour, minutes):
  return hour + (minutes/60.0)

def predicate_dst(month, day, hour):
  "returns true if dst applies and false if not"
  return false

# Step 1 - Calculate the fractional year in degrees
def frac_year(month, day, hour, minutes):
  day_num = day_number(month, day)
  frac_hour = frac_hours(hour, minutes)
  if predicate_dst:
    frac_hour = frac_hour + 1
  else:
    pass
  frac_year = (360/365.25)*(day_num + (frac_hour/24.0))
  return frac_year




