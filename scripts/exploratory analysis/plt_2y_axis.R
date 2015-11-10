#plot function
plt_2y_axis <- function(date,var1,main,xlabel,ylabel){
  
  mindate = "/5/1"  
  maxdate = "/11/1"
  mindate = as.Date(paste(date,mindate,sep = ""))
  maxdate = as.Date(paste(date,maxdate,sep=""))
  
  pathpng <- file.path(plotfolder,paste(main, ".png", sep = ""))
#   pathpdf <- file.path(plotfolder,paste(main, ".pdf", sep = ""))
#   pdf(file=pathpdf)
  png(file=pathpng)
  
  #For testing
  #   date="2007"
  #   var1="Tavg"
  #   main="Infection rate and Average Temperature 2007"
  #   xlabel="WNV infection rate [%]"
  #   ylabel="Average Temperature"
  opar <- par()
  on.exit(suppressWarnings(par(opar)))
  par(mar=c(6, 4, 4, 5))
  ymax1=1.95
  ymax2 = max(as.numeric(train_weather.stat1[,eval(var1)]))
  
  data=subset(train_weather.stat1,format(Date,format="%Y")==date)
  name = sprintf("Mosquito season %s", date) 
  
  #First plot
  # 1.1*max(data$WNV_ratio)
  plot(x=data$Date, y=data$WNV_ratio, ylim=c(0,1.1*ymax1),
       col='blue', type='l',
       xlim=c(mindate,maxdate),
       main=main, sub='', xlab='', ylab='',
       xaxt='n', yaxt='n', lwd=1.5)
  
  
  axis(2, pretty(c(0, 1.1*max(data$WNV_ratio))), col='blue')
  mtext(xlabel, side=2, col="blue", line=2.5)
  
  #Keep recent plot active to host second plot
  par(new=T)
  
  #Second plot into first plots window
  #1.1*max(as.numeric(data[,eval(var1)]))
  plot(x=data$Date, y=data[,eval(var1)], ylim=c(0,1.1*ymax2),
       col='red', type='l', lwd=1.5,
       xlim=c(mindate,maxdate),
       xlab='', ylab='',
       xaxt='n', axes=F)
  
  # manually label, farther out than normal
  mtext(ylabel, side=4, col="red", line=2.5)
  
  # label the y axis
  axis(4, pretty(c(0, 1.1*max(as.numeric(data[,eval(var1)])))), col='red')
  
  
  # put X axis labels on first date present in each quarter
  mindate = "/5/1"  
  maxdate = "/11/1"
  mindate = paste(date,mindate,sep = "")
  maxdate = paste(date,maxdate,sep="")
  time = seq(as.Date(mindate), as.Date(maxdate), "month")
  axis.Date(1, at=time, labels=format(time, '%b-%U'))
  abline(v=time, col='grey', lwd=0.5)
  
  #close plot window! --sometimes not working properly
  dev.off()
  
}