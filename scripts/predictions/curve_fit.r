# Modified version of https://www.kaggle.com/oconnoda/predict-west-nile-virus/population-model
# Author of the original version - David O'Connor
# Covered by the Apache 2.0 open source license

options(warn = -1)
library(plyr)
library(ggplot2)

train = read.csv("~/Code/data_mining_lab/input_data/train.csv",stringsAsFactors=FALSE)
train$Date = as.Date(train$Date)
lt = as.POSIXlt(train$Date)
woy = floor((lt$yday - lt$wday + 7) / 7)
# implicit model of the data collection
hits = lt$wday == 1 & lt$year == 113 & woy == 27
train$Date[hits] = train$Date[hits] - 3
hits = lt$wday == 1 & lt$year == 111 & woy == 28
train$Date[hits] = train$Date[hits] - 3
hits = lt$wday == 1 & lt$year == 111 & woy == 30
train$Date[hits] = train$Date[hits] - 3
hits = lt$wday == 1 & lt$year == 111 & woy == 37
train$Date[hits] = train$Date[hits] - 3
hits = lt$wday == 4 & lt$year == 111 & woy == 35
train$Date[hits] = train$Date[hits] + 1
hits = lt$wday == 2 & lt$year == 109 & woy == 22
train$Date[hits] = train$Date[hits] - 4
hits = lt$wday == 1 & lt$year == 109 & woy == 24
train$Date[hits] = train$Date[hits] - 3
hits = lt$wday == 1 & lt$year == 109 & woy == 25
train$Date[hits] = train$Date[hits] - 3
hits = lt$wday == 1 & lt$year == 109 & woy == 26
train$Date[hits] = train$Date[hits] - 3
hits = lt$wday == 1 & lt$year == 109 & woy == 27
train$Date[hits] = train$Date[hits] - 3
hits = lt$wday == 1 & lt$year == 109 & woy == 28
train$Date[hits] = train$Date[hits] - 3
hits = lt$wday == 1 & lt$year == 109 & woy == 30
train$Date[hits] = train$Date[hits] - 3
hits = lt$wday == 2 & lt$year == 109 & woy == 34
train$Date[hits] = train$Date[hits] - 4
hits = lt$wday == 1 & lt$year == 109 & woy == 37
train$Date[hits] = train$Date[hits] - 3
hits = lt$wday == 5 & lt$year == 107 & woy == 25
train$Date[hits] = train$Date[hits] + 3

train$Date = as.POSIXlt(train$Date)
train$Year = as.factor(train$Date$year+1900)
train$Week = floor((train$Date$yday - train$Date$wday + 7) / 7)
ftrain = ddply(train,.(Week,Year),summarize,WnvCount=sum(WnvPresent))
ftrain = ftrain[order(ftrain$Year,ftrain$Week),]

ggplot(ftrain,aes(x=Week,y=WnvCount,colour=Year))+ geom_line()  

ftrain$WnvCount2 = filter(ftrain$WnvCount,c(0.25,0.5,0.25))
ftrain$WnvCount2[is.na(ftrain$WnvCount2)] = ftrain$WnvCount[is.na(ftrain$WnvCount2)]
ftrain$WnvCount = ftrain$WnvCount2
ymax = ddply(ftrain,.(Year),summarize,yearMax=max(WnvCount))
ftrain = merge(ftrain,ymax,by="Year")
ftrain$WnvCountScaled = ftrain$WnvCount / ftrain$yearMax

ggplot(ftrain,aes(x=Week,y=WnvCountScaled))+ geom_line() + facet_wrap(~Year,ncol=2)

fittedtrain = ftrain[1,]
fittedtrain$fitted = 0
for (iYear in unique(ftrain$Year)) {
  ytrain = subset(ftrain, iYear == Year)
  m = nls(WnvCountScaled ~ I(height * exp(-(Week - center)^2/width)), data=ytrain, start=list(height = 2.5, center = 33, width = 4))
  ytrain$fitted = m$m$fitted()
  fittedtrain = rbind(fittedtrain,ytrain)
}
ftrain = fittedtrain[-1,]

ggplot(ftrain,aes(x=Week,y=WnvCountScaled))+ geom_line() +
  geom_line(aes(x=Week,y=fitted),color="red", linetype=2) + facet_wrap(~Year,ncol=2)

wnvModel = function(data) {
  model = function(Week,height,center,width) {
    height * exp(-(Week - center)^2/width)
  }
  df = unique(data[,c("Year","Week","WnvCount")])
  p = wnvFit(df,df)
  pars.all = p$pars
  pars = list()
  for (pyear in 2007:2014) {
    i = pyear - 2006
    if (pyear %in% c(2007,2009,2011,2013)) {
      dfy = subset(data,pyear==Year)
      p = wnvFit(dfy,dfy)
      pars[[i]] = p$pars
    }
    else {
      pars[[i]] = pars.all
    }
  }
  pars[[2]]["height"] = 5
  pars[[2]]["center"] = 34.5
  pars[[2]]["width"] = 10
  pars[[4]]["height"] = 5
  pars[[4]]["center"] = 31.4
  pars[[4]]["width"] = 12.14
  pars[[6]]["height"] = 28
  pars[[6]]["center"] = 31.6
  pars[[6]]["width"] = 11.5
  pars[[8]]["height"] = 9
  pars[[8]]["center"] = 33.5
  pars[[8]]["width"] = 12.14
  
  list(model=model,pars=pars)
}

wnvFit = function(train,test) {
  # A fifth degree polynomial also fits well
  #m = lm(WnvCount~poly(Week,degree=5,raw=TRUE),data=train)
  #p = predict(m,newdata=test)
  m = nls(WnvCount ~ I(height * exp(-(Week - center)^2/width)), data=train, start=list(height = 3, center = 33, width = 8))
  p = predict(m,newdata=test)  
  list(p=p,pars=m$m$getPars())
}

predictWnv = function(train,test) {
  m = wnvModel(train)
  wnvPredict(m,test)
}

wnvPredict = function(m,data) {
  p = numeric(nrow(data))
  for (i in 1:nrow(data)) {
    pars = m$pars[[data$Year[i]-2006]]
    p[i] = m$model(data$Week[i],pars["height"],pars["center"],pars["width"])
  }
  p
}

test = read.csv("~/Code/data_mining_lab/input_data/test.csv",stringsAsFactors=FALSE)
test$Date = as.POSIXlt(test$Date)
test$Year = test$Date$year+1900
test$Week = floor((test$Date$yday - test$Date$wday + 7) / 7)
test$WnvCount = predictWnv(ftrain,test)
ggplot(test,aes(x=Week,y=WnvCount))+ geom_line() + facet_wrap(~Year,ncol=2)

