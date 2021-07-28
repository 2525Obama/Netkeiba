import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler


df = pd.read_csv("test.csv",encoding="cp932")

# 4着以下は4として表示
clip_rank = lambda x: x if x < 4 else 4

df["着順"] = df["rank"].map(clip_rank)

df.drop(["rank","RaceID","horse_name","time_2","passage_rate","jockey_name","jockey_id","trainer_name","horse_id","trainer_id"],axis=1,inplace=True)
results_d = pd.get_dummies(df)

X = results_d.drop(["着順"],axis=1)
Y = results_d["着順"]

X_train,X_test,Y_train,Y_test = train_test_split(X,Y,stratify=Y,test_size=0.2,random_state=0)

# データ数が偏るため整える
rank_1 = Y_train.value_counts()[1]
rank_2 = Y_train.value_counts()[2]
rank_3 = Y_train.value_counts()[3]
rank_4 = Y_train.value_counts()[4]
rus = RandomUnderSampler(sampling_strategy={1:rank_1,2:rank_2,3:rank_3,4:rank_1}, random_state=71)
X_trainR,Y_trainR = rus.fit_resample(X_train,Y_train)


model = LogisticRegression()
model.fit(X_trainR,Y_trainR)

print(model.score(X_train,Y_train),model.score(X_test,Y_test))

Y_pred = model.predict(X_test)

pred_df = pd.DataFrame({"pred":Y_pred, "actual":Y_test})
print(pred_df["pred"].value_counts())
print(pred_df["actual"])