# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 21:33:07 2024

@author: oem
"""

 #Soru1 : miuul_gezinomi.xlsx dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz..
 #Soru2:Kaç unique şehir vardır? Frekansları nedir?
 #Soru3:Kaç unique Concept vardır?
 #Soru4:Hangi Concept’den kaçar tane satış gerçekleşmiş?
 #Soru5:Şehirlere göre satışlardan toplam ne kadar kazanılmış?
 #Soru6:Concept türlerine göre göre ne kadar kazanılmış?
 #Soru7:Şehirlere göre PRICE ortalamaları nedir?
 #Soru8:Conceptlere göre PRICE ortalamaları nedir?
 #Soru9:Şehir-Concept kırılımındaPRICE ortalamaları nedir?

import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x:"%.2f" % x)
df =  pd.read_excel("C:/Users/oem/Desktop/miuul_gezinomi.xlsx")
print(df.head())
print(df.shape)
print(df.info())
df["SaleCityName"].nunique()
df["SaleCityName"].value_counts()
df["ConceptName"].nunique()
df["ConceptName"].value_counts()
df.groupby("SaleCityName").agg({"Price" : "sum"})
df.groupby("ConceptName").agg({"Price" : "sum"})
df.groupby("SaleCityName").agg({"Price" : "mean"})
df.groupby("ConceptName").agg({"Price" : "mean"})
df.groupby(["SaleCityName","ConceptName"] ).agg({"Price" : "mean"})
#SaleCheckInDayDiffdeğişkenini kategorik bir değişkene çeviriniz.
bins = [-1, 7, 30, 90, df["SaleCheckInDayDiff"].max()]
labels = ["Last Minuters", "Potential Planners", "Planners", "Early Bookers"] 
df["EB_score"] = pd.cut(df["SaleCheckInDayDiff"], bins, labels=labels)
df.head(50).to_excel("eb_scorew.xlsx", index=False)  
# COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
df.groupby(["SaleCityName", "ConceptName", "EB_score"]).agg({"Price" : ["mean", "count"]})
df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price" : ["mean", "count"]})       
df.groupby(["SaleCityName", "ConceptName", "CInDay"]).agg({"Price" : ["mean", "count"]})    
#City-Concept-Season kırılımının çıktısını PRICE'a göre sıralayınız.
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x:"%.2f" % x)
df =  pd.read_excel("C:/Users/oem/Desktop/miuul_gezinomi.xlsx")
agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": ["mean", "count"]})

# 'Price' ortalamasına göre sıralama yap
agg_df = agg_df.sort_values(by=("Price", "mean"), ascending=False)

# İlk 20 satırı göster
print(agg_df.head(20))
# Indekste yer alan isimleri değişken ismine çeviriniz.
agg_df.reset_index(inplace=True)
agg_df.head()
# Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
agg_df["sales_level_based"] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].agg(lambda x: "_".join(x).upper(), axis=1)
agg_df.head()
#Yeni müşterileri (personaları) segmentlere ayırınız.
agg_df["SEGMENT"] = pd.qcut(agg_df[("Price", "mean")], 4, labels=["D", "C", "B", "A"])
agg_df.head()
agg_df.groupby("SEGMENT").agg({("Price", "mean"): [ "mean", "max", "sum"]})
#Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini  tahmin ediniz.
agg_df.sort_values(by=("Price", "mean"))
# Antalya’da herşey dahil ve yüksek sezonda tatil yapmak isteyen bir kişinin ortalama ne kadar gelir kazandırması beklenir?
new_user = "ANTALYA_HERŞEY DAHIL_HIGH"
agg_df[agg_df["sales_level_based"] == new_user]
#Girne’de yarım pansiyon bir otele düşük sezonda giden bir tatilci hangi segmentte yer alacaktır?
new_user = "GIRNE_ODA + KAHVALTI_LOW"
agg_df.loc[agg_df["sales_level_based"] == new_user, "SEGMENT"]


