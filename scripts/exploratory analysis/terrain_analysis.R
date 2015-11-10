require(lubridate)
require(sqldf)
        
traindata=read.csv("/Users/bhartimunjal/workspace/WestNileVirusPrediction/Scripts1/train_with_terrain_attr_threshold.csv")
#year_2007=sqldf("select Date, Trap, NumMosquitos, Latitude,Longitude,Forests,WaterBodies, WnvPresent from traindata where Date like '2007%' group by Date, Trap");


yearsArray=c(2007,2009,2011,2013) ;

for (year in yearsArray)
{
    print("###################################################");
    print(year);
    q <- sprintf("select Date, Trap, NumMosquitos, Latitude, Longitude, Forests, WaterBodies, CASE WHEN sum(WnvPresent) =  0 THEN 0 else 1 END as WNV from traindata where  Date like '%s' group by Date, Latitude,Longitude",paste(year,"%",sep = ''));
    print(q);
    year_new  <- sqldf(q);
    year_new1=sqldf("select Latitude,Longitude, sum(WNV) as s, count(WNV) as c,sum(WNV)*1.0/count(WNV)*1.0  as WnvPresentRatioForTrap, Forests,WaterBodies from  year_new  group by Latitude,Longitude") ;    
    
    avginfectionrateMapForForest=NULL ;
    avginfectionrateMapForRivers=NULL ;
    avginfectionrateMapForForestRivers=NULL ;
    
    thresholdArray=c(500,1000,1500,2000,2500,3000,3500,4000, 4500,5500,6000,6500,7000,7500);
    count=1 ;    

    for (threshold in thresholdArray){
      queryForest <- sprintf("select (sum(s)*1.0/sum(c)*1.0) as AvgInfectionRate,%s from  year_new1  where Forests < %s ", threshold,threshold)
      print(queryForest);
      avginfectionrateMapForForest[count]=sqldf(queryForest) ;
      
      queryRiver <- sprintf("select (sum(s)*1.0/sum(c)*1.0) as AvgInfectionRate,%s from  year_new1  where WaterBodies < %s ", threshold,threshold)
      print(queryRiver);
      avginfectionrateMapForRivers[count]=sqldf(queryRiver) ;
      
      queryForestRiver <- sprintf("select (sum(s)*1.0/sum(c)*1.0) as AvgInfectionRate,%s from  year_new1  where WaterBodies < %s and Forests < %s  ", threshold,threshold,threshold)
      print(queryForestRiver);
      avginfectionrateMapForForestRivers[count]=sqldf(queryForestRiver) ;
      
      count=count+1 ;
    }
    
    names(avginfectionrateMapForForest) <- thresholdArray ;
    names(avginfectionrateMapForRivers) <- thresholdArray ;
    names(avginfectionrateMapForForestRivers) <- thresholdArray ;
    
    png(filename=paste(year,"_Forest.png",sep=''));
    plot(names(avginfectionrateMapForForest),avginfectionrateMapForForest, ylim=c(0,0.25) ,type="o",col="green",xlab="Threshold Distance From Forest", ylab="Average WNV Infection Rate", main= paste("Avg Infection rate Vs Thresh.Distance From Forest for Year",year));

    dev.off() ;
    
    png(filename=paste(year,"_WaterBodies.png",sep=''));
    plot(names(avginfectionrateMapForRivers),avginfectionrateMapForRivers, type="o",ylim=c(0,0.25),col="blue",xlab="Threshold Distance From River", ylab="Average WNV Infection Rate", main= paste("Avg Infection rate Vs Thresh Distance From River for Year",year));
    
    
    
    dev.off() ; 
    
    png(filename=paste(year,"_ForestWaterBodies.png",sep=''));
    plot(names(avginfectionrateMapForForestRivers),avginfectionrateMapForForestRivers,ylim=c(0,0.25), type="o",col="red",xlab="Threshold Distance From River and Forest", ylab="Average WNV Infection Rate", main= paste("Avg Infection Vs Distance From River & Forest for Year",year));
    
    dev.off() ; 
    print("############################################");

}









#year_2009=sqldf("select * from traindata where Date like '2009%'");  

#year_2011=sqldf("select * from traindata where Date like '2011%'");











#date_format = "%Y-%m-%d" ;
#traindata$Date=as.Date(traindata$Date,date_format);

##For whole data
#table(traindata$threshold_3000,traindata$WnvPresent)
#barplot(prop.table(table( traindata$threshold_3000,traindata$WnvPresent),2), beside=TRUE, col=c("green","red"), legend=rownames(table(traindata$threshold_3000,traindata$WnvPresent)));

##Year wise 



