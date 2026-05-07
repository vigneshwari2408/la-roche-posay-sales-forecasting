import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# 1. LOAD REAL DATA FROM EXCEL
# ─────────────────────────────────────────────
df_raw = pd.read_excel("../excel/La_Roche_Posay_Sales_Forecasting.xlsx")

learn = df_raw.iloc[0:59].copy()
learn = learn.rename(columns={
    "Jour Semaine" : "day_of_week",
    "Holidays ?"   : "is_holiday",
    "Week-end ?"   : "is_weekend",
    "Newsletter ?" : "newsletter",
    "Sales"        : "sales"
})
learn = learn[["Date","day_of_week","is_holiday","is_weekend","newsletter","sales"]].dropna()
learn = learn.reset_index(drop=True)

test = df_raw.iloc[61:76].copy()
test.columns = df_raw.iloc[60].values
test = test.rename(columns={
    "Jour Semaine" : "day_of_week",
    "Holidays ?"   : "is_holiday",
    "Week-end ?"   : "is_weekend",
    "Newsletter ?" : "newsletter",
    "REAL VALUE"   : "sales"
})
test = test[["day_of_week","is_holiday","is_weekend","newsletter","sales"]].dropna()
test = test.reset_index(drop=True)

forecast = df_raw.iloc[76:88].copy()
forecast.columns = df_raw.iloc[60].values
forecast_dates = df_raw.iloc[76:88]["Date"].values
forecast = forecast.rename(columns={
    "Jour Semaine" : "day_of_week",
    "Holidays ?"   : "is_holiday",
    "Week-end ?"   : "is_weekend",
    "Newsletter ?" : "newsletter",
})
forecast = forecast[["day_of_week","is_holiday","is_weekend","newsletter"]].reset_index(drop=True)

features = ["is_holiday", "is_weekend", "newsletter"]

X_train = learn[features].values.astype(float)
y_train = learn["sales"].values.astype(float)
X_test  = test[features].values.astype(float)
y_test  = test["sales"].values.astype(float)
X_fore  = forecast[features].values.astype(float)

print("=" * 58)
print("  La Roche-Posay — Real Sales Data")
print("=" * 58)
print(f"  Learning rows : {len(learn)}  ({learn['Date'].iloc[0].date()} to {learn['Date'].iloc[-1].date()})")
print(f"  Testing rows  : {len(test)}  (Nov 29 to Dec 13 2021)")
print(f"  Forecast rows : {len(forecast)}  (Dec 14 to Dec 25 2021)")
print(f"  Mean sales (train): {y_train.mean():.0f}")

def mape(real, forecast_vals):
    real = np.array(real, dtype=float)
    forecast_vals = np.array(forecast_vals, dtype=float)
    return np.mean(np.abs(forecast_vals - real) / real) * 100

# MODEL 1 — GLOBAL AVERAGE
global_avg = y_train.mean()
pred_avg   = np.full(len(y_test), global_avg)
mape_avg   = mape(y_test, pred_avg)
print("\n" + "=" * 58)
print("  MODEL 1 — Global Average")
print("=" * 58)
print(f"  Global average (train) : {global_avg:.2f}")
print(f"  MAPE                   : {mape_avg:.2f}%")

# MODEL 2 — DAY-OF-WEEK AVERAGE
dow_avg  = learn.groupby("day_of_week")["sales"].mean()
pred_dow = test["day_of_week"].map(dow_avg).values
mape_dow = mape(y_test, pred_dow)
print("\n" + "=" * 58)
print("  MODEL 2 — Day-of-Week Average")
print("=" * 58)
print("  Avg sales by day (1=Mon ... 7=Sun):")
print("  " + str(dow_avg.round(0).astype(int).to_dict()))
print(f"  MAPE : {mape_dow:.2f}%")

# MODEL 3 — LINEAR REGRESSION
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
pred_lr  = lr_model.predict(X_test)
mape_lr  = mape(y_test, pred_lr)
print("\n" + "=" * 58)
print("  MODEL 3 — Linear Regression")
print("=" * 58)
print(f"  Coefficients : {dict(zip(features, lr_model.coef_.round(1)))}")
print(f"  Intercept    : {lr_model.intercept_:.2f}")
print(f"  MAPE         : {mape_lr:.2f}%")

# MODEL 4 — PYTORCH LSTM
print("\n" + "=" * 58)
print("  MODEL 4 — PyTorch LSTM")
print("=" * 58)

SEQ_LEN = 7
BATCH_SIZE = 8
EPOCHS = 100
HIDDEN = 32

all_data = pd.concat([
    learn[["day_of_week","is_holiday","is_weekend","newsletter","sales"]],
    test[["day_of_week","is_holiday","is_weekend","newsletter","sales"]]
], ignore_index=True)

sales_min = y_train.min()
sales_max = y_train.max()
def normalize(x):   return (x - sales_min) / (sales_max - sales_min)
def denormalize(x): return x * (sales_max - sales_min) + sales_min

norm_sales = normalize(all_data["sales"].values.astype(np.float32))
feat_all   = all_data[features].values.astype(np.float32)

def make_sequences(sales, feats, seq_len):
    X, y = [], []
    for i in range(len(sales) - seq_len):
        seq = sales[i:i+seq_len].reshape(-1, 1)
        f   = feats[i:i+seq_len]
        X.append(np.concatenate([seq, f], axis=1))
        y.append(sales[i+seq_len])
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

X_seq, y_seq = make_sequences(norm_sales, feat_all, SEQ_LEN)
n_train = len(learn) - SEQ_LEN
X_tr = torch.tensor(X_seq[:n_train])
y_tr = torch.tensor(y_seq[:n_train])
X_te = torch.tensor(X_seq[n_train:])
y_te_norm = y_seq[n_train:]

train_loader = DataLoader(TensorDataset(X_tr, y_tr), batch_size=BATCH_SIZE, shuffle=True)

class SalesLSTM(nn.Module):
    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.lstm   = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.linear = nn.Linear(hidden_size, 1)
    def forward(self, x):
        out, _ = self.lstm(x)
        return self.linear(out[:, -1, :]).squeeze()

model     = SalesLSTM(input_size=1+len(features), hidden_size=HIDDEN)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.MSELoss()

for epoch in range(EPOCHS):
    model.train()
    for xb, yb in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(xb), yb)
        loss.backward()
        optimizer.step()
    if (epoch + 1) % 20 == 0:
        model.eval()
        with torch.no_grad():
            val_pred = model(X_te).numpy()
        val_mape = mape(denormalize(y_te_norm), denormalize(val_pred))
        print(f"  Epoch {epoch+1:3d}/{EPOCHS}  |  Val MAPE: {val_mape:.2f}%")

model.eval()
with torch.no_grad():
    pred_lstm_norm = model(X_te).numpy()
pred_lstm = denormalize(pred_lstm_norm)
mape_lstm = mape(denormalize(y_te_norm), pred_lstm)
print(f"\n  MAPE (LSTM) : {mape_lstm:.2f}%")

# FORECAST Dec 14-25
fore_lr = lr_model.predict(X_fore)
print("\n" + "=" * 58)
print("  FUTURE FORECAST — Dec 14-25 2021 (Linear Regression)")
print("=" * 58)
for date, pred in zip(forecast_dates, fore_lr):
    print(f"  {str(date)[:10]}  ->  Forecast: {pred:.0f} units")

# FINAL SUMMARY
print("\n" + "=" * 58)
print("  FINAL RESULTS SUMMARY")
print("=" * 58)
results = {
    "Global Average"     : mape_avg,
    "Day-of-Week Average": mape_dow,
    "Linear Regression"  : mape_lr,
    "PyTorch LSTM"       : mape_lstm,
}
for name, val in results.items():
    beat = " beats LR!" if name == "PyTorch LSTM" and val < mape_lr else ""
    print(f"  {name:<25} MAPE = {val:6.2f}%{beat}")
print("=" * 58)
