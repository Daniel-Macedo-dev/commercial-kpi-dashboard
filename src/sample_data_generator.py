import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

REGIONS = ["North", "Northeast", "Midwest", "Southeast", "South"]
CHANNELS = ["Hospital", "Distributor", "Retail", "Online", "Clinic"]
PRODUCT_LINES = [
    "Medical Devices",
    "Hospital Solutions",
    "Consumer Health Simulation",
    "Clinical Products",
    "Patient Care",
]
PRODUCTS = {
    "Medical Devices": ["SurgiPro X1", "MedScan 200", "FlexCath Pro", "OrthoFix Plus"],
    "Hospital Solutions": ["HospCore Suite", "BedCare System", "IV FlowMaster", "WoundShield"],
    "Consumer Health Simulation": ["HealthTrack Kit", "VitaBalance", "CareSimPack", "WellnessSet Pro"],
    "Clinical Products": ["ClinAssay 500", "DiagnoKit Elite", "LabReady Pro", "PathoClear"],
    "Patient Care": ["ComfortBrace", "RecoverEase", "NutriSupport Kit", "MobilityAid Plus"],
}
REPS = [
    "Alice Santos", "Bruno Martins", "Carla Oliveira", "Diego Pereira",
    "Elena Costa", "Fabio Lima", "Gabriela Rocha", "Henrique Silva",
    "Isabela Ferreira", "João Mendes",
]
_CHANNEL_MULTIPLIER = {
    "Hospital": 1.4,
    "Distributor": 1.1,
    "Retail": 0.9,
    "Online": 0.8,
    "Clinic": 1.0,
}


def generate_dataset(n_rows: int = 400, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    random.seed(seed)

    start_date = datetime(2023, 1, 1)
    date_range_days = (datetime(2024, 12, 31) - start_date).days

    rows = []
    for _ in range(n_rows):
        date = start_date + timedelta(days=int(rng.integers(0, date_range_days)))
        region = random.choice(REGIONS)
        channel = random.choice(CHANNELS)
        product_line = random.choice(PRODUCT_LINES)
        product = random.choice(PRODUCTS[product_line])
        rep = random.choice(REPS)

        base_revenue = rng.uniform(5_000, 80_000)
        revenue = round(base_revenue * _CHANNEL_MULTIPLIER[channel], 2)
        target = round(revenue * rng.uniform(0.85, 1.20), 2)

        opportunities = int(rng.integers(5, 50))
        conversions = int(rng.integers(1, opportunities + 1))
        units_sold = int(rng.integers(1, 100))
        discount = round(float(rng.uniform(0.0, 0.25)), 4)

        rows.append({
            "Date": date.date(),
            "Region": region,
            "Channel": channel,
            "Product Line": product_line,
            "Product": product,
            "Sales Representative": rep,
            "Revenue": revenue,
            "Target": target,
            "Opportunities": opportunities,
            "Conversions": conversions,
            "Units Sold": units_sold,
            "Discount": discount,
        })

    return pd.DataFrame(rows).sort_values("Date").reset_index(drop=True)


def save_dataset(output_path: Path | None = None) -> Path:
    if output_path is None:
        output_path = Path(__file__).parent.parent / "data" / "sample_commercial_data.xlsx"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = generate_dataset()
    df.to_excel(output_path, index=False, engine="openpyxl")
    print(f"Dataset saved: {output_path} ({len(df)} rows)")
    return output_path


if __name__ == "__main__":
    save_dataset()
