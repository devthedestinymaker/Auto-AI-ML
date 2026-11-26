import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

# Carbon emission factors (kg CO2 per dollar spent)
# Based on real-world LCA (Life Cycle Assessment) studies
EMISSION_FACTORS = {
    'Groceries': 1.2,           # Food production, packaging, transport
    'Dining & Takeout': 2.0,    # Restaurant energy, food waste, packaging
    'Gas & Fuel': 3.5,          # Vehicle manufacturing, fuel extraction, combustion
    'Flights & Travel': 5.0,    # Aviation fuel, airport operations
    'Clothing & Apparel': 1.8,  # Textile production, dyeing, transport
    'Public Transit': 0.4,      # Bus/train energy efficiency
    'Utilities & Energy': 2.8,  # Electricity generation (varies by grid)
    'Electronics': 1.1,         # Manufacturing, rare earth mining
    'Entertainment': 0.9,       # Streaming, events, gaming
    'Subscriptions': 0.7,       # Digital services, cloud computing
}

def generate_transactions(n_transactions=1000):
    """
    Generate synthetic transaction data.
    
    Args:
        n_transactions: Number of transactions to generate
    
    Returns:
        DataFrame with transactions
    """
    # Start date: 1 year ago from today
    start_date = datetime(2024, 11, 20)
    
    transactions = []
    
    for i in range(n_transactions):
        # Random date within the year
        days_offset = random.randint(0, 365)
        transaction_date = start_date + timedelta(days=days_offset)
        
        # Random category
        category = random.choice(list(EMISSION_FACTORS.keys()))
        
        # Generate amount based on category (more realistic distributions)
        if category in ['Groceries', 'Dining & Takeout']:
            amount = np.random.lognormal(mean=3.5, sigma=0.8)  # Skewed right
        elif category in ['Gas & Fuel', 'Flights & Travel']:
            amount = np.random.lognormal(mean=4.0, sigma=1.0)  # Higher variance
        else:
            amount = np.random.lognormal(mean=3.0, sigma=0.7)  # Lower amounts
        
        amount = round(amount, 2)
        
        # Generate merchant name
        merchants = {
            'Groceries': ['Whole Foods', 'Trader Joes', 'Safeway', 'Costco', 'Walmart'],
            'Dining & Takeout': ['McDonalds', 'Starbucks', 'Chipotle', 'Dominoes', 'Local Cafe'],
            'Gas & Fuel': ['Shell', 'Exxon', 'Chevron', 'BP'],
            'Flights & Travel': ['Delta', 'United', 'American', 'Southwest'],
            'Clothing & Apparel': ['Nike', 'H&M', 'Zara', 'Uniqlo', 'Target'],
            'Public Transit': ['City Transit', 'Metro', 'Bus'],
            'Utilities & Energy': ['PG&E', 'Con Edison', 'Duke Energy'],
            'Electronics': ['Best Buy', 'Apple Store', 'Amazon Tech'],
            'Entertainment': ['Netflix', 'Spotify', 'Cinema', 'GameStop'],
            'Subscriptions': ['Adobe', 'Microsoft', 'Amazon Prime']
        }
        merchant = random.choice(merchants.get(category, ['Generic Store']))
        
        transactions.append({
            'date': transaction_date,
            'merchant': merchant,
            'category': category,
            'amount': amount
        })
    
    return pd.DataFrame(transactions)


def calculate_carbon_footprint(df):
    """
    Calculate carbon footprint for each transaction.
    
    Args:
        df: DataFrame with transactions
    
    Returns:
        DataFrame with carbon footprint column added
    """
    df = df.copy()
    df['emission_factor'] = df['category'].map(EMISSION_FACTORS)
    df['carbon_kg'] = df['amount'] * df['emission_factor']
    return df

def main():
    """Generate and save transaction data."""
    print("Generating synthetic transaction data...")
    
    # Generate transactions
    df = generate_transactions(1000)
    
    # Calculate carbon footprint
    df = calculate_carbon_footprint(df)
    
    # Save to CSV using path relative to this script file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.abspath(os.path.join(script_dir, '..', '..', 'data', 'transactions.csv'))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"[SUCCESS] Generated {len(df)} transactions")
    print(f"[SUCCESS] Saved to {os.path.abspath(output_path)}")
    print(f"\n[SUMMARY] Statistics:")
    print(f"   Total spending: ${df['amount'].sum():,.2f}")
    print(f"   Total carbon footprint: {df['carbon_kg'].sum():,.2f} kg CO2")
    print(f"   Average daily footprint: {df['carbon_kg'].sum()/365:.2f} kg CO2/day")

if __name__ == "__main__":
    main()
    