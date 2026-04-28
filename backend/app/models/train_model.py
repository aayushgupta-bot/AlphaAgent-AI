import asyncio
import os
import joblib
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

from app.services.data_service import DataService
from app.services.indicator_service import IndicatorService


async def train_and_save_model():
    print("=" * 60)
    print("AlphaAgent AI — Model Training (Returns-Based)")
    print("=" * 60)

    data_service = DataService()
    indicator_service = IndicatorService()

    # ── Fetch multi-stock data for generalization ──────────────────────────
    tickers = ["AAPL", "MSFT", "TSLA", "NVDA", "GOOGL"]
    all_frames = []

    for ticker in tickers:
        print(f"\nFetching data for {ticker}...")
        try:
            df = await data_service.get_ohlcv(ticker, interval="1d", period="5y")
            if df.empty:
                print(f"  ⚠ Empty dataset for {ticker}, skipping.")
                continue
            df = await indicator_service.calculate_indicators(df)
            df.dropna(inplace=True)

            # ── TARGET: next-day percentage return ────────────────────────
            df["target"] = df["close"].pct_change().shift(-1)
            df.dropna(inplace=True)

            all_frames.append(df)
            print(f"  ✓ {ticker}: {len(df)} rows")
        except Exception as e:
            print(f"  ✗ {ticker} failed: {e}")

    if not all_frames:
        print("Error: No data collected. Aborting.")
        return

    combined = pd.concat(all_frames, ignore_index=True)
    print(f"\nCombined dataset: {combined.shape[0]} rows")

    # ── Feature / target split ────────────────────────────────────────────
    feature_cols = [col for col in combined.columns if col not in ["target", "date", "Date"]]
    X = combined[feature_cols]
    y = combined["target"]

    # Clip extreme outlier returns (>10% daily) to reduce noise
    y = y.clip(-0.10, 0.10)

    print(f"Feature columns ({len(feature_cols)}): {feature_cols[:8]}...")
    print(f"Target stats — mean: {y.mean():.6f}, std: {y.std():.6f}")

    # ── Train / test (chronological per stock, combined shuffle ok here) ──
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=True, random_state=42
    )
    print(f"Train: {X_train.shape[0]} rows | Test: {X_test.shape[0]} rows")

    # ── Train ─────────────────────────────────────────────────────────────
    print("\nTraining XGBoost Regressor on returns...")
    model = XGBRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    )
    model.fit(X_train, y_train)

    # ── Evaluate ──────────────────────────────────────────────────────────
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    # Direction accuracy: did we get the sign right?
    sign_match = np.sign(predictions) == np.sign(y_test.values)
    direction_accuracy = sign_match.mean()

    # Distribution of predicted directions
    n_up = (predictions > 0.002).sum()
    n_down = (predictions < -0.002).sum()
    n_neutral = len(predictions) - n_up - n_down

    print(f"\n{'─' * 40}")
    print(f"Test MSE:              {mse:.8f}")
    print(f"Test MAE:              {mae:.6f}")
    print(f"Direction Accuracy:    {direction_accuracy:.2%}")
    print(f"Predicted UP:          {n_up} ({n_up/len(predictions):.1%})")
    print(f"Predicted DOWN:        {n_down} ({n_down/len(predictions):.1%})")
    print(f"Predicted NEUTRAL:     {n_neutral} ({n_neutral/len(predictions):.1%})")
    print(f"{'─' * 40}")

    # ── Save ──────────────────────────────────────────────────────────────
    os.makedirs("app/models", exist_ok=True)
    model_path = "app/models/xgb.pkl"
    joblib.dump(model, model_path)
    joblib.dump(feature_cols, "app/models/feature_cols.pkl")

    print(f"\n✓ Model saved to {model_path}")
    print("✓ Feature columns saved to app/models/feature_cols.pkl")


if __name__ == "__main__":
    asyncio.run(train_and_save_model())
