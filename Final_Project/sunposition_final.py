#!/usr/bin/env python
# -*- coding: utf-8 -*-

from digifab import *
import math
import numpy
import re
import solid
import solid.utils


## AUXILIAR FUNCTIONS ##
def DCM_to_degrees(a_str):
  # The equation: Decimal Degrees = Degrees + minutes/60 + seconds/3600
  split_str = re.split("º|´|´´|'|''| |", a_str) #including all sort of possible characters
  filt_str = map(float, (filter(str.isdigit, split_str))) #filtering the digits and transforming into numbers
  str_degrees= filt_str[0] + (filt_str[1]/60) + (filt_str[2]/3600)
  if "S" in a_str or "W" in a_str:
    str_degrees *= -1
  else:
    str_degrees
  return str_degrees

def pts_to_vec (pt_a, pt_b):
  start = numpy.asarray(pt_a)
  end = numpy.asarray(pt_b)
  vec = end - start
  return vec

########################


## The SUN class ##

class Sun:
  """
  A class that describes the Sun, its position, and that generates a visualization of it.
  Important Attributes:
    Passed as arguments:
      latitude ->  in degrees (int or float) or in string format with the following format (e.g.;): 48º 49' 0'' N)
      longitude -> in degrees (int or float) or in string format with the following format (e.g.;): 2º 17' 23'' E)
      month -> the number of the month in integers or its name as a string (e.g.; 1 or "January")
      day -> in integers
      hours -> in integers
      minutes -> in integers
      r -> optional argument for visualization. It corresponds to the radius of the sphere. Its default is 40m (a float or integer).
      DST -> optional argument of the boolean type. DST triggers daylight savings or not. Its default is set to False.
    Computed (with init):
      sunDec -> Sun Declination
      TC -> Time correction
      SHA -> Solar Hour Angle
      Altitude -> Sun Altitude or Sun Elevation Angle
      Zenith -> Sun Zenith Angle
  Methods:
    SunPosition_Spherical -> returns the sun position in spherical coordinates as a list - [r, ]
    SunPosition_Cart -> returns the sun position in cartesian coordinates
    viz -> generates an openScad model for visualization of the sun position in a sky dome.
  """

  def __init__(self, latitude, longitude, time_zone, month, day, hours, minutes, r= 40.0, DST= False):
    self.latitude = latitude
    self.longitude = longitude
    self.time_zone = time_zone
    self.month = month
    self.day = day
    self.hours = hours
    self.minutes = minutes
    self.r = r
    self.DST = DST

    nDays_2009 = 40178 #we will assume for the sake of simplicity that we are at 2010
    Julian_constant = 2415018.5 #if we are in 2010 this is the Julian Constant according with NOOA
    

    def day_number(month, day):
      if month == 1 or "anuary" in str(month):
        day_num = day
      elif month == 2 or "ebruary" in str(month):
        day_num = 31 + day
      elif month == 3 or "arch" in str(month):
        day_num = (31+28) + day
      elif month == 4 or "pril" in str(month):
        day_num = (31+28+31) + day
      elif month == 5 or "ay" in str(month):
        day_num = (31+28+31+30) + day
      elif month == 6 or "une" in str(month):
        day_num = (31+28+31+30+31) + day
      elif month == 7 or "uly" in str(month):
        day_num = (31+28+31+30+31+30) + day
      elif month == 8 or "ugust" in str(month):
        day_num = (31+28+31+30+31+30+31) + day
      elif month == 9 or "eptember" in str(month):
        day_num = (31+28+31+30+31+30+31+31) + day
      elif month == 10 or "ctober" in str(month):
        day_num = (31+28+31+30+31+30+31+31+30) + day
      elif month == 11 or "ovember" in str(month):
        day_num = (31+28+31+30+31+30+31+31+30+31) + day
      else:
        day_num = (31+28+31+30+31+30+31+31+30+31+30) + day
      return day_num

    dayNum = day_number(self.month, self.day)

    def longitude_to_degrees(lg):
      if type(lg) is str: 
        return DCM_to_degrees(lg)
      else:
        return lg

    self.longitude_degrees = longitude_to_degrees(self.longitude)

    def latitude_to_degrees (lat):
      if type(lat) is str:
        return DCM_to_degrees(lat)
      else:
        return lat

    self.latitude_degrees = latitude_to_degrees(self.latitude)

    """  
    def predicate_dst(self):
      "returns true if dst applies and false if not"
      "should use self.month, self.day, self.hour"
      return false
    """

    def frac_hours(hour, minutes):
      return hour + (minutes/60.0)

    fracHour = frac_hours(self.hours, self.minutes)

    # Calculate the fractional year in degrees
    def frac_year(month, day, hour, minutes, frac_hour):
      day_num = day_number(self.month, self.day)
      if self.DST == True:
        frac_hour = frac_hour + 1
      else:
        pass
      frac_year = (360/365.25)*(day_num + (frac_hour/24.0))
      return frac_year

    fracYear = frac_year(self.month, self.day, self.hours, self.minutes, self.fracHour)

    #Calculate the Julian Day
    def Julian_Day (day_num, fracH, timeZone):
      return (nDays_2009+day_num) + Julian_constant + (fracH/24.0) - timeZone/24.0

    julianDay = Julian_Day(dayNum, fracHour, self.time_zone) 

    #Calculate the Julian Century
    def Julian_century(jd):
      return (jd - 2451545)/36525.0

    julianCentury = Julian_century(julianDay)

    #Calculate the Geometric Mean Longitude of the Sun [deg - º]
    def GMLong_Sun(jc):
      return (280.46646 + jc *(36000.76983 + jc * 0.0003032))%360

    gml_Sun = GMLong_Sun(julianCentury) 

    #Calculate the Geometric Mean Anomaly of the Sun [deg - º]
    def GMAnom_Sun(jc):
      return 357.52911 + jc * (35999.05029 - 0.0001537 * jc)

    gma_Sun = GMAnom_Sun(julianCentury)

    #Calculate the Eccentric Earth Orbit
    def Ecc_Orbit(jc):
      return 0.016708634 - jc * (0.000042037 + 0.0000001267 * jc)

    eccOrb = Ecc_Orbit(julianCentury)

    #Calculate the Sun Eq of Ctr
    def Sun_eq_Ctr(jc, geoanom_sun):
      return math.sin(math.radians(geoanom_sun)) * (1.914602 - jc * (0.004817 + 0.000014 * jc)) + \
                math.sin(math.radians(2*geoanom_sun)) * (0.019993 - 0.000101 * jc) + \
                  math.sin(math.radians(3*geoanom_sun)) * 0.000289

    sunEqCtr = Sun_eq_Ctr(julianCentury, gma_Sun)

    #Calculate the Sun True Longitude [deg - º]
    def Sun_true_long(gmlongSun, sunEq):
      return gmlongSun + sunEq

    sunTrueLong = Sun_true_long(gml_Sun, sunEqCtr)

    #Calculate the Sun True Anomaly [deg - º]
    def Sun_true_anom(geoanom_sun, sunEq):
      return geoanom_sun + sunEq

    sunTrueAnom = Sun_true_anom(gma_Sun, sunEqCtr)

    #Calculate the Sun Rad Vector [AUs]
    def Sun_rad_vec(ecc_orb, sunTanom):
      return (1.000001018 * (1 - ecc_orb * ecc_orb)) / (1 + ecc_orb * math.cos(math.radians(sunTanom)))

    sunRadVec = Sun_rad_vec (eccOrb, sunTrueAnom)

    #Calculate the Sun App Long [deg - º]
    def Sun_app_long (sunTlong, jc):
      return sunTlong - 0.00569 - 0.00478 * math.sin(math.radians(125.04 - 1934.136 * jc))

    sunAppLong = Sun_app_long (sunTrueLong, julianCentury)

    #Calculate the Mean Obliq Ecliptic [deg - º]
    def Mean_Obliq_Ecl (jc):
      return 23+(26+((21.448 - jc * (46.815 + jc *(0.00059 - jc * 0.001813))))/60)/60.0

    mObliqEcl = Mean_Obliq_Ecl(julianCentury)

    #Calculate the Obliq Correction [deg - º]
    def Obliq_corr (meanObliEc, jc):
      return meanObliEc + 0.00256 * math.cos(math.radians(125.04 - 1934.136 * jc))

    obliqCorr = Obliq_corr(mObliqEcl, julianCentury)

    #Calculate Sun Rt Ascen [deg - º]
    def Sun_rt_ascen (sunApplg, oblcorr):
      a = math.cos(math.radians(sunApplg))
      b = math.cos(math.radians(oblcorr)) * math.sin(math.radians(sunApplg))
      return math.degrees(math.atan2(b, a)) #because in Excel they switch the order natively in ATAN2

    sunRtAscen = Sun_rt_ascen(sunAppLong, obliqCorr)

    #Calculate Sun Declination [deg - º]
    def sun_dec (oblcorr, sunApplg):
      return math.degrees(math.asin(math.sin(math.radians(oblcorr)) * math.sin(math.radians(sunAppLong))))

    self.sunDec = sun_dec(obliqCorr, sunAppLong



    """  
    # Step 3 - Time correction
    def time_correction(fracYear):
      return (0.004297+0.107029*math.cos(math.radians(fracYear))-
                1.837877*math.sin(math.radians(fracYear))-
                  0.837378*math.cos(math.radians(2*fracYear))-2.340475*math.sin(math.radians(2*fracYear)))

    self.TC = time_correction(self.fracYear)

    # Step 4 - Solar Hour Angle Calculation
    def SolarHourAngle(hour, longitude, tc): #tc stands for time_correction
      SolarHAngle = (((hour-12)*15) + longitude + tc)
      if SolarHAngle > 180:
        SolarHAngle += -360
      elif SolarHAngle < -180:
        SolarHAngle += 360
      else:
        SolarHAngle = SolarHAngle
      return SolarHAngle

    self.SHA = SolarHourAngle(self.fracHour, self.longitude_degrees, self.TC)

    # Step 5 - Sun Zenith Angle and Elevation angle
    def SunZenith_ElevationAngle(latitude, declination, sha): #sha stands for solar hour angle
      cos_sza = math.sin(math.radians(latitude)) *\
                  math.sin(math.radians(declination)) + math.cos(math.radians(latitude)) *\
                    math.cos(math.radians(declination)) * math.cos(math.radians(sha))
      if cos_sza > 1:
        cos_sza = 1
      elif cos_sza < -1:
        cos_sza = -1
      else:
        cos_sza = cos_sza
      zenith = math.degrees(math.acos((cos_sza))) # or zenith angle - it is correct
      altitude = 90 - zenith # or Elevation angle - it is correct
      return altitude, zenith

    self.Altitude = SunZenith_ElevationAngle(self.latitude_degrees, self.sunDec, self.SHA)[0]
    self.Zenith = SunZenith_ElevationAngle(self.latitude_degrees, self.sunDec, self.SHA)[1]

    # Step 6 - Sun Azimuth
    def SunAzimuth (latitude, declination, zenith):
      cos_az = (math.sin(math.radians(declination)) - math.sin(math.radians(latitude)) *
                 math.cos(math.radians(zenith)))/(math.cos(math.radians(latitude)) * math.sin(math.radians(zenith)))
      return (math.degrees(math.acos(cos_az))) #correction to the algorithm in order to make az= 90 north - in this way we align north with the y-axis

    self.Azimuth = SunAzimuth(self.latitude_degrees, self.sunDec, self.Zenith)

  """

  ### METHODS ###
  ###############

  def SunPosition_Spherical(self):
    """
    The Position of the sun in spherical coordinates.
    It returns the list - [radius, Azimuth, Zenith]
    """
    return [self.r, round(self.Azimuth, 4), round(self.Zenith, 4)] 

  def SunPosition_Cart(self):
    """
    The Position of the sun in cartesian coordinates.
    It returns the list - [x, y, z]
    """
    x = round((self.r * math.sin(math.radians(self.Zenith)) * math.cos(math.radians(self.Azimuth))),4)
    y = round((self.r * math.sin(math.radians(self.Zenith)) * math.sin(math.radians(self.Azimuth))),4)
    z = round((self.r * math.cos(math.radians(self.Zenith))), 4)

    return [x,y,z]

  def viz(self,position):
    """
    Generates a OpenScad model to visualize the sun position
    """

    ## Generating the hemisphere ##
    starting_sphere = solid.sphere(self.r, segments= 64)
    box_sub = solid.utils.down(((self.r * 2 + 10)/2))(solid.cube((self.r * 2 + 10), center= True))
    hemisphere = starting_sphere - box_sub
    hemisphere = PolyMesh(generator= hemisphere).simplified()
    #hemisphere = (solid.utils.color([0.75,0.75,0.75,0.1]))(hemisphere.get_generator()) #this sucks...need to do this way in order do render
    #hemisphere = PolyMesh(generator= hemisphere)

    ## Generate the sphere for the sun ##
    sun_sphere = solid.sphere(5, segments= 64)
    vector = position
    sun_sphere = (solid.translate(vector))(sun_sphere)
    sun_sphere = PolyMesh(generator= sun_sphere).simplified()

    L1 = Layer(hemisphere, name= "hem", color=[200,200,200,1000])
    L2 = Layer(sun_sphere, name="sun", color='yellow')

    B1 = Block([L1, L2])

    return B1.show(is_2d= False)

    