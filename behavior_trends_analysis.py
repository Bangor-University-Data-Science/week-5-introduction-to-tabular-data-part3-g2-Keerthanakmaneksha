import pandas as pd

def import_data(filename: str) -> pd.DataFrame:
    if filename.endswith('.csv'):
        df = pd.read_csv(filename)
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        df = pd.read_excel(filename)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
    return df

def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=['CustomerID'])
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    return df

def loyalty_customers(df: pd.DataFrame, min_purchases: int) -> pd.DataFrame:
    customer_purchases = df.groupby('CustomerID').size().reset_index(name='purchase_count')
    loyal_customers = customer_purchases[customer_purchases['purchase_count'] >= min_purchases]
    return loyal_customers

def quarterly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['quarter'] = df['InvoiceDate'].dt.to_period('Q')
    df['revenue'] = df['Quantity'] * df['UnitPrice']
    quarterly_revenue_df = df.groupby('quarter')['revenue'].sum().reset_index()
    quarterly_revenue_df.columns = ['quarter', 'total_revenue']
    return quarterly_revenue_df

def high_demand_products(df: pd.DataFrame, top_n: int) -> pd.DataFrame:
    product_demand = df.groupby('Description')['Quantity'].sum().reset_index()
    top_products = product_demand.nlargest(top_n, 'Quantity')
    return top_products

def purchase_patterns(df: pd.DataFrame) -> pd.DataFrame:
    product_summary = df.groupby('Description').agg(
        avg_quantity=('Quantity', 'mean'),
        avg_unit_price=('UnitPrice', 'mean')
    ).reset_index()
    return product_summary

def answer_conceptual_questions() -> dict:
    answers = {
        "Q1": {"A"},
        "Q2": {"B"},
        "Q3": {"C"},
        "Q4": {"A", "B"},
        "Q5": {"A"}
    }
    return answers

if __name__ == "__main__":
    filename = "Customer_Behavior.xlsx"
    df = import_data(filename)
    
    filtered_df = filter_data(df)
    
    loyal_customers_df = loyalty_customers(filtered_df, min_purchases=10)
    print("Loyal Customers:\n", loyal_customers_df)
    
    quarterly_revenue_df = quarterly_revenue(filtered_df)
    print("Quarterly Revenue:\n", quarterly_revenue_df)
    
    top_products_df = high_demand_products(filtered_df, top_n=5)
    print("Top High-Demand Products:\n", top_products_df)
    
    purchase_summary_df = purchase_patterns(filtered_df)
    print("Purchase Patterns:\n", purchase_summary_df)
    
    conceptual_answers = answer_conceptual_questions()
    print("Conceptual Answers:\n", conceptual_answers)