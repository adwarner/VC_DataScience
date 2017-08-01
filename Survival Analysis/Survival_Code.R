library(survival)
setwd("~/Documents/VC Soccer/Survival Analysis/")
data1 <- read.csv("Scores.csv")


survobj <- with(data1, Surv(Time,Scored))
fit.km = survfit(survobj ~ Win.Loss, data = data1)
plot(fit.km, col = c("red", "green"), lty = c(1,2))
title(main = 'KM-Curve Wins/Loss Based On \n Time of First Opposing Goal', 
      xlab = 'Minutes', 
      ylab = 'Survival Rate')
legend("bottomleft",
       legend = c("Loss", "Win"), lty = c(1,2),
       title = "Treatment Group", bty = "n", col = c("red", "green"))
survdiff(survobj ~ Win.Loss, data = data1)
