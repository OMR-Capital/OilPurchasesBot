# Purchases Bot

## Description

This bot help to manage purchases for retail company.

There are three roles:

1. Superuser - can create and delete admins and employees, also has all admin functionality.
2. Admin - can see statistic of purchases and approve purchases from employees.
3. Employee - can create new purchases applications.

To get access for functionality of one of this roles you should call login form by `/start` command and then login with specific access key

## Deployment

1. Create bot via BotFather
2. Click on `Deploy to Deta`

    [![Deploy](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy?repo=https://github.com/mamsdeveloper/PurchasesBot)
3. Enter env variables (GOOGLE section may be skipped)
4. Set webhook:

    ```bash
        curl -X POST https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook
    -H "Content-Type: application/json"
    -d '{"url": "https://<example-bot>.deta.sh/webhook", "secret_token": "<TELEGRAM_SECRET>"}'
    ```

5. Create new superuser with `/create_root`. Enjoy!
6. For activate statistics at GoogleSheets create secret key file by that [instruction](https://docs.gspread.org/en/latest/oauth2.html#enable-api-access-for-a-project) and then load it to DetaStorage by **bot/statistics/google_sheets/load_key_file** or by another way. Create Google spreadsheet and add just created service account to editors.

## Thanks

[aiogram](https://github.com/aiogram)

[Deta](https://github.com/deta)
