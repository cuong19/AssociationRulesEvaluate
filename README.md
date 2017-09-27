# AssociationRulesEvaluate
A Python app for evaluating the rules mined with the app AssociationRulesMiner
https://github.com/cuong19/AssociationRulesMiner

## What does this app do?
This app use the 20% of transactions to evaluate the rules mined with the other 80%.
For each item in a transaction it will check if there is a rule, and is the consequent item in the rule present in the transaction.

## How to use
- Note: All the program codes are in the **src** folder
- First create a **config.yml** file with the template in the folder
- Edit the config file to connect to your database instances
- Run the **app.py** and the rules mined will be evaluated
- The output to screen will include:
    - Number of times a rule is found for an item
    - Number of times no rules found for an item
    - Number of times a rule is applicable for an item set
    - Number of times no rules are applicable for an item set
