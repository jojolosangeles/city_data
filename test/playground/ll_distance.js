<!-- hide this script tag's contents from old browsers
// Copyright 1997 Ed Williams. All rights reserved

decpl=4  // Dec places of minutes output
//**************CD****************
function ClearFormCD(){

    document.InputFormCD.lat1.value = "34.0386";
    document.InputFormCD.lat2.value = "34.0415";
    document.InputFormCD.lon1.value = "118.2201";
    document.InputFormCD.lon2.value = "118.2196";
    document.OutputFormCD.crs12.value = "";
    document.OutputFormCD.crs21.value = "";
    document.OutputFormCD.d12.value = "";

    distance_in_feet(34.0386,-118.2201,34.0415,-118.2196);

}

function ComputeFormCD(){
  refactor1(document.InputFormCD.NS1, document.InputFormCD.NS2, document.InputFormCD.EW1, document.InputFormCD.EW2,
            document.InputFormCD.lat1, document.InputFormCD.lat2, document.InputFormCD.lon1, document.InputFormCD.lon2)
}

function ns(val) {
  return (val < 0) ? -1 : 1
}

function ew(val) {
  return (val < 0) ? -1 : 1
}

function distance_in_feet(lat1, lon1, lat2, lon2) {
  //console.log(`distance_in_feet(${lat1}, ${lon1}, ${lat2}, ${lon2})`)
  return refactor1(ns(lat1), ns(lat2), ew(lon1), ew(lon2), Math.abs(lat1), Math.abs(lat2), Math.abs(lon1), Math.abs(lon2))
}

function refactor1(doc_ns1, doc_ns2, doc_ew1, doc_ew2, doc_lat1, doc_lat2, doc_lon1, doc_lon2) {
  var signlat1,signlat2,signlon1,signlon2,dc
  var lat1,lat2,lon1,lon2
  var d,crs12,crs21
  var argacos
  var a,invf
  /* Input and validate data */
  signlat1=signlatlon(doc_ns1)
  signlat2=signlatlon(doc_ns2)
  signlon1=signlatlon(doc_ew1)
  signlon2=signlatlon(doc_ew2)

  lat1=(Math.PI/180)*signlat1*doc_lat1
  lat2=(Math.PI/180)*signlat2*doc_lat2
  lon1=(Math.PI/180)*signlon1*doc_lon1
  lon2=(Math.PI/180)*signlon2*doc_lon2

  dc=185200.0/30.48 /* get distance conversion factor */

  // spherical code
  cd=crsdist(lat1,lon1,lat2,lon2) // compute crs and distance
  crs12 =cd.crs12*(180/Math.PI)
  crs21 =cd.crs21*(180/Math.PI)
  d=cd.d*(180/Math.PI)*60*dc  // go to physical units

  return d
}

function crsdist(lat1,lon1,lat2,lon2){ // radian args
/* compute course and distance (spherical) */
with (Math){

  d=acos(sin(lat1)*sin(lat2)+cos(lat1)*cos(lat2)*cos(lon1-lon2))

  if ((d==0.) || (lat1==-(PI/180)*90.)){
     crs12=2*PI
  } else if (lat1==(PI/180)*90.){
     crs12=PI
  } else {
     argacos=(sin(lat2)-sin(lat1)*cos(d))/(sin(d)*cos(lat1))
     if (sin(lon2-lon1) < 0){
       crs12=acosf(argacos)
     }
     else{
       crs12=2*PI-acosf(argacos)
     }
  }
  if ((d==0.) || (lat2==-(PI/180)*90.)){
     crs21=0.
  } else if (lat2==(PI/180)*90.){
     crs21=PI
  }else{
     argacos=(sin(lat1)-sin(lat2)*cos(d))/(sin(d)*cos(lat2))
     if (sin(lon1-lon2)<0){
       crs21=acosf(argacos)
     }
     else{
       crs21=2*PI-acosf(argacos)
     }
  }
}
out=new MakeArray(0)
out.d=d
out.crs12=crs12
out.crs21=crs21
return out
}


function signlatlon(selection){
  return selection > 0 ? 1 : -1
}

function MakeArray(n){
   this.length=n
   for (var i=1;i<=n;i++){
     this[i]=0
   }
   return this
}

function acosf(x){ /* protect against rounding error on input argument */
if (Math.abs(x) >1){
    x /=Math.abs(x)
  }
return Math.acos(x)
}


function feet_to_lat_units(feet, starting_latitude, fixed_longitude) {
  var starting_decimal = .1
  var current_decimal = .1
  var value = distance_in_feet(starting_latitude, fixed_longitude, starting_latitude + current_decimal, fixed_longitude)
  while (Math.round(value) > feet) {
    current_decimal *= starting_decimal;
    value = distance_in_feet(starting_latitude, fixed_longitude, starting_latitude + current_decimal, fixed_longitude)
  }
  var factor = Math.floor(feet/value)
  var d1_adjustment = factor*current_decimal
  var d1latitude = starting_latitude + d1_adjustment
  var amount = distance_in_feet(starting_latitude, fixed_longitude, d1latitude, fixed_longitude)
  current_decimal *= starting_decimal
  value = amount
  d2factor = 0
  while (value < feet) {
    d2factor += 1
    value = distance_in_feet(starting_latitude, fixed_longitude, d1latitude + d2factor*current_decimal, fixed_longitude)
  }
  var d2_adjustment = d2factor*current_decimal
  amount = distance_in_feet(starting_latitude, fixed_longitude, starting_latitude + d1_adjustment + d2_adjustment, fixed_longitude)
  return d1_adjustment + d2_adjustment
}

function feet_to_lon_units(feet, fixed_latitude, starting_longitude) {
  var starting_decimal = .1
  var current_decimal = .1
  var value = distance_in_feet(fixed_latitude, starting_longitude, fixed_latitude, starting_longitude + current_decimal)
  while (Math.round(value) > feet) {
    current_decimal *= starting_decimal;
    value = distance_in_feet(fixed_latitude, starting_longitude, fixed_latitude, starting_longitude + current_decimal)
  }
  var factor = Math.floor(feet/value)
  var d1_adjustment = factor*current_decimal
  var d1longitude = starting_longitude + d1_adjustment
  var amount = distance_in_feet(fixed_latitude, starting_longitude, fixed_latitude, starting_longitude + d1_adjustment)
  current_decimal *= starting_decimal
  value = amount
  d2factor = 0
  while (value < feet) {
    d2factor += 1
    value = distance_in_feet(fixed_latitude, starting_longitude, fixed_latitude, starting_longitude + d1_adjustment + d2factor*current_decimal)
  }
  var d2_adjustment = d2factor*current_decimal
  amount = distance_in_feet(fixed_latitude, starting_longitude, fixed_latitude, starting_longitude + d1_adjustment + d2_adjustment)
  return d1_adjustment + d2_adjustment
}
// -- done hiding from old browsers -->
console.log("START")
var result = distance_in_feet(34.0386,-118.2201,34.0415,-118.2196);
console.log("RESULT=" + result)

var EXAMPLE_LATITUDE = 34.0386
var EXAMPLE_LONGITUDE = -118.2201
var lat_units_for_feet = feet_to_lat_units(1000, EXAMPLE_LATITUDE, EXAMPLE_LONGITUDE);
result = distance_in_feet(EXAMPLE_LATITUDE, EXAMPLE_LONGITUDE, EXAMPLE_LATITUDE + lat_units_for_feet, EXAMPLE_LONGITUDE)
console.log(`RESULT should be near 1000, it is ${result}`)
var lon_units_for_feet = feet_to_lon_units(500, EXAMPLE_LATITUDE, EXAMPLE_LONGITUDE)
result = distance_in_feet(EXAMPLE_LATITUDE, EXAMPLE_LONGITUDE, EXAMPLE_LATITUDE, EXAMPLE_LONGITUDE + lon_units_for_feet)
console.log(`RESULT should be near 500, it is ${result}`)

console.log("END OF TEST")
