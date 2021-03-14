# Data Analyst - Assignment 
![Image](https://uploads-ssl.webflow.com/5e820230603d2720689c8249/5ee4f9c2e4be3a3e46943568_logo_text_alternate-p-500.png)

## Goal
Client subscriptions request process the data to come up with a list of subscriptions we will upload to our app with the following format:
```json
[
	{
	    "name": "Burger King",
	    "periodType": "monthly",
	    "periodValue": 150,
	    "nextPaymentDate": "2021-04-01T09:28:38.274Z",
	    "externalID": "client_bk"
	},
	{
	    "name": "Mc Donald's",
	    "periodType": "quarterly",
	    "periodValue": 350,
	    "nextPaymentDate": "2021-03-22T17:28:05.301Z",
	    "externalID": "client_mcd"
	}
]
```


### Data sources :scroll:
 - Database with the invoice information.
    - Provided by Capchase formatted as a `.xlsx` file.
 
 ## **Installation**
Use the package manager conda to install the following libraries:

```bash
conda install pandas
```
 ### Requirements :arrow_forward:
 - Data analysis:
    - Pandas
###  **Folder structure**
```
└── project
    ├── __trash__
    ├── .gitignore
    ├── .env
    ├── requeriments.txt
    ├── README.md
    ├── main_script.py
    ├── notebooks
    │   ├── notebook1.ipynb
    │   └── notebook2.ipynb
    ├── package1
    │   ├── module1.py
    │   └── module2.py
    └── data
    └── results
```
# Output :pushpin:
.json file with account data.

