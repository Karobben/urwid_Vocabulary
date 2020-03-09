#!/usr/bin/env R
library(ggplot2)
library(ggrepel)
library(ggcal)

A <- read.table("En.log")
A$Date = paste(A[[2]],A[[3]],A[[5]],sep="_")
TB = A[c(13,6:12)]

# total
TB = data.frame(Sum=t(t(colSums(TB[2:8]))))
X = c("Wrods_All","Words","Words_Wrong","Sentence","Sentence_Wrong","Sentence_Words","Sentence_WrongWords")
row.names(TB) = X
ggplot(TB) +
  geom_bar(aes(x=X,y=log(1+Sum),group=X,fill=X),stat='identity') +
  geom_text(aes(x=X,y=log(1+max(Sum))*0.75,label=Sum),color="red",size=2) +
  coord_polar(theta ="x", start = pi/3) +
  theme(axis.title=element_blank(),
    axis.text.y=element_blank(),
    axis.text.x=element_text(size=5),
    axis.ticks=element_blank(),legend.position="None" ) +
  labs(title="Today")+
  theme(panel.grid.major =element_blank(),
    panel.grid.minor = element_blank(),
    panel.background = element_blank(),
    axis.line = element_blank(),
    title=element_text(size=7,vjust=0)) #+
    #expand_limits(x=c(0,10))


ggsave("Total.png",height=1.8,width=1.8)


TB = A[c(13,6:12)]
X = c("Date","Wrods_All","Words","Words_Wrong","Sentence","Sentence_Wrong","Sentence_Words","Sentence_WrongWords")
colnames(TB) = X
TB=TB[c(1,3,4)]

List = unique(TB[[1]])
i = List[1]
tmp = TB[which(TB[[1]] == i ),]
Result <- data.frame(Date=i,t(colSums(tmp[2:3])))

for(i in List[2:length(List)]){
tmp = TB[which(TB[[1]] == i ),]
tmp <- data.frame(Date=i,t(colSums(tmp[2:3])))
Result <- rbind(Result,tmp)
}

Result$MisRate = Result[[3]]/Result[[2]] *max(Result[[2]])
Result$MisRateT = paste(round(Result[[3]]/Result[[2]],4)*100,"%",sep='')

ggplot(Result,aes(x=Date)) +
geom_bar(aes(y=Words, fill = Words),stat='identity')+
geom_text(aes(y=Words+20,label= Words)) +
geom_point(aes(y=MisRate))+
geom_text_repel(aes(y=MisRate+10,label= MisRateT),color='#FA8072') +
geom_smooth(aes(y=MisRate,group=1,color='Mistake Ratio')) +
theme_light()+
theme(axis.text.x= element_text(angle=-45,hjust=0))

ggsave('Total2.png',width=15,height=5)

Result[[1]] = as.Date(Result[[1]],"%B_%d_%Y")
ggcal(Result[[1]], Result[[2]]) +
    scale_fill_gradient2(low="#4575b4", mid="#ffffbf", high="#d73027", midpoint=0)
ggsave('Total2_Cal.png')
