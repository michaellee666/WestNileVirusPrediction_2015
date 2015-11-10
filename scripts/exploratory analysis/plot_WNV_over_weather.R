#Load 
library(ggmap)

#source plot function to workspace
source('~/coding/datamining/github_dmproj/data_mining_lab/scripts/Rscripts/plt_2y_axis.R')

setwd("~/datamining/github_dmproj/data_mining_lab/input_data")
plotfolder = ("~/coding/datamining/github_dmproj/data_mining_lab/plots/")

#Load data sets
traindata=read.csv("train.csv")
#traindata$Date <-
weatherdata=read.csv("weather.csv")
spraydata=read.csv("spray.csv")

MosquitoCountsByDate=aggregate(cbind(NumMosquitos,WnvPresent)~Date,data=traindata,sum)
MosquitoCountsVsWeather=merge(weatherdata,MosquitoCountsByDate)
MosquitoCountsVsWeather$Date <- as.Date(as.character(MosquitoCountsVsWeather$Date), "%Y-%m-%d")

#separate data from two weather stations
train_weather.stat1 <- subset(MosquitoCountsVsWeather,Station==1)
train_weather.stat1$WNV_ratio <- train_weather.stat1$WnvPresent/train_weather.stat1$NumMosquitos*100
train_weather.stat2 <- subset(MosquitoCountsVsWeather,Station==2)

#train_weather.stat1$MSQ_normalized <- train_weather.stat1$NumMosquitos/trap_cnt
#trap_cnt = rle(as.character(Week))$length

plt_2y_axis("2007","Tavg","Infection rate and Average Temperature 2007","WNV infection rate [%]","Average daily temperature [°F]")
plt_2y_axis("2009","Tavg","Infection rate and Average Temperature 2009","WNV infection rate [%]","Average daily temperature [°F]")
plt_2y_axis("2011","Tavg","Infection rate and Average Temperature 2011","WNV infection rate [%]","Average daily temperature [°F]")
plt_2y_axis("2013","Tavg","Infection rate and Average Temperature 2013","WNV infection rate [%]","Average daily temperature [°F]")
plt_2y_axis("2007","PrecipTotal","Infection rate and Preciptitation 2007","WNV infection rate [%]","Total daily preciptitation")
plt_2y_axis("2009","PrecipTotal","Infection rate and Preciptitation 2009","WNV infection rate [%]","Total daily preciptitation")
plt_2y_axis("2011","PrecipTotal","Infection rate and Preciptitation 2011","WNV infection rate [%]","Total daily preciptitation")
plt_2y_axis("2013","PrecipTotal","Infection rate and Preciptitation 2013","WNV infection rate [%]","Total daily preciptitation")
plt_2y_axis("2007","AvgSpeed","Infection rate and Average windspeed 2007","WNV infection rate [%]","Average daily windspeed")
plt_2y_axis("2009","AvgSpeed","Infection rate and Average windspeed 2009","WNV infection rate [%]","Average daily windspeed")
plt_2y_axis("2011","AvgSpeed","Infection rate and Average windspeed 2011","WNV infection rate [%]","Average daily windspeed")
plt_2y_axis("2013","AvgSpeed","Infection rate and Average windspeed 2013","WNV infection rate [%]","Average daily windspeed")
plt_2y_axis("2007","WetBulb","Infection rate and Wet Bulb Temperature 2007","WNV infection rate [%]","Average daily Wet Bulb Temperature")
plt_2y_axis("2009","WetBulb","Infection rate and Wet Bulb Temperature 2009","WNV infection rate [%]","Average daily Wet Bulb Temperature")
plt_2y_axis("2011","WetBulb","Infection rate and Wet Bulb Temperature 2011","WNV infection rate [%]","Average daily Wet Bulb Temperature")
plt_2y_axis("2013","WetBulb","Infection rate and Wet Bulb Temperature 2013","WNV infection rate [%]","Average daily Wet Bulb Temperature")
plt_2y_axis("2007","StnPressure","Infection rate and Standard pressure 2007","WNV infection rate [%]","Daily Standard Pressure")
plt_2y_axis("2009","StnPressure","Infection rate and Standard pressure 2009","WNV infection rate [%]","Daily Standard Pressure")
plt_2y_axis("2011","StnPressure","Infection rate and Standard pressure 2011","WNV infection rate [%]","Daily Standard Pressure")
plt_2y_axis("2013","StnPressure","Infection rate and Standard pressure 2013","WNV infection rate [%]","Daily Standard Pressure")

as.numeric(levels(f))[f]


