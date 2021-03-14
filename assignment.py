import pandas as pd
import json

FREQUENCY = {
    'daily': {
        'min': pd.Timedelta(hours=0),
        'max': pd.Timedelta(hours=24),
        'time_delta': pd.Timedelta(days=1)
    },
    'weekly': {
        'min': pd.Timedelta(days=1),
        'max': pd.Timedelta(days=7),
        'time_delta': pd.Timedelta(days=7)
    },
    'monthly': {
        'min': pd.Timedelta(days=7),
        'max': pd.Timedelta(days=31),
        'time_delta': pd.Timedelta(days=30)
    },
    'quarterly': {
        'min': pd.Timedelta(days=30),
        'max': pd.Timedelta(days=92),
        'time_delta': pd.Timedelta(days=90)
    },
    'semesterly': {
        'min': pd.Timedelta(days=90),
        'max': pd.Timedelta(days=181),
        'time_delta': pd.Timedelta(days=181)
    },
    'annually': {
        'min': pd.Timedelta(days=181),
        'max': pd.Timedelta(days=365),
        'time_delta': pd.Timedelta(days=365)
    }
}


def stadarize(df):
    df['responsetext'] = df['responsetext'].str.lower()
    df['time'] = pd.to_datetime(df['time'], format='%Y%m%d%H%M%S')
    return df


def get_company(row):
    if pd.notnull(row["first_name"]) and pd.notnull(row["last_name"]):
        return f'{row["first_name"]} {row["last_name"]}'
    return row["account"]


def filter_status(df):
    status_filter = (df['status'] == 'complete') | (df['status'] == 'unknown')
    response_filter = df['response'] == 'success'
    responsetext_filter = df['responsetext'] == 'approved'
    total_filter = status_filter & response_filter & responsetext_filter
    return df[total_filter]


def get_period_type(mean_invoice_time_interval):
    if FREQUENCY['daily']['min'] < mean_invoice_time_interval <= FREQUENCY['daily']['max']:
        return 'daily'
    elif FREQUENCY['weekly']['min'] < mean_invoice_time_interval <= FREQUENCY['weekly']['max']:
        return 'weekly'
    elif FREQUENCY['monthly']['min'] < mean_invoice_time_interval <= FREQUENCY['monthly']['max']:
        return 'monthly'
    elif FREQUENCY['quarterly']['min'] < mean_invoice_time_interval <= FREQUENCY['quarterly']['max']:
        return 'quarterly'
    elif FREQUENCY['semesterly']['min'] < mean_invoice_time_interval <= FREQUENCY['semesterly']['max']:
        return 'semesterly'
    else:
        return 'annually'


def get_next_payment_date(row):
    time_delta = FREQUENCY[row['period_type']]['time_delta']
    return row["last_time"] + time_delta


def generate_json(df, path):
    df = df[['company', 'period_type', 'period_value', 'next_payment_date', 'account']]
    df = df.rename(columns={
        'company': 'name',
        'period_type': 'periodType',
        'period_value': 'periodValue',
        'next_payment_date': 'nextPaymentDate',
        'account': 'externalID'
    })

    result = df.to_json(orient="records")
    parsed = json.loads(result)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(parsed, f, ensure_ascii=False, indent=4)


def process_accounts(invoices_df):
    accounts = list(invoices_df['account'].unique())
    results = []

    for account in accounts:
        invoices_for_account_df = invoices_df[invoices_df['account'] == account].sort_values(by='time', ascending=True)
        (total_rows, _) = invoices_for_account_df.shape

        if total_rows >= 2:
            invoices_for_account_df = invoices_for_account_df.iloc[-2:]

        invoices_for_account_df['invoice_time_interval'] = invoices_for_account_df['time'].diff()
        mean_invoice_time_interval = invoices_for_account_df['invoice_time_interval'].iloc[-1]
        last_time = invoices_for_account_df['time'].iloc[-1]
        period_value = invoices_for_account_df['amount'].iloc[-1]
        company = invoices_for_account_df['company'].iloc[-1]
        results.append((account, mean_invoice_time_interval, last_time, period_value, company))

    return results


def main():
    invoices_df = pd.read_excel('data/test_invoices_20210305.xlsx', index_col=0)
    invoices_df = stadarize(invoices_df)
    invoices_df["company"] = invoices_df.apply(get_company, axis=1)
    invoices_df = filter_status(invoices_df)

    results = process_accounts(invoices_df)

    results_df = pd.DataFrame(results,
                              columns=['account', 'mean_invoice_time_interval', 'last_time', 'period_value', 'company'])

    results_df["period_type"] = results_df["mean_invoice_time_interval"].apply(get_period_type)
    results_df["next_payment_date"] = results_df.apply(get_next_payment_date, axis=1)

    generate_json(results_df, 'result/results.json')


if __name__ == "__main__":
    main()
