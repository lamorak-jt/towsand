# Account Reference

Structured list of accounts with identifiers for automated data capture.
DB account names must match `src/db/seed.py` exactly.

---

## Interactive Brokers

| DB Account Name    | Account ID  | Currency | Type    | Portal URL                                      |
|--------------------|-------------|----------|---------|------------------------------------------------|
| IB Trading AUD     | U19190510   | AUD      | Trading | https://www.interactivebrokers.com/portal        |

**Data capture:** Flex Web Service (`towsand ib import-flex`)

---

## CommSec

| DB Account Name    | Account ID  | Currency | Type    | Portal URL                                      |
|--------------------|-------------|----------|---------|------------------------------------------------|
| CommSec Trading    | 57493105    | AUD      | Trading | https://www2.commsec.com.au/Private/Portfolio    |

**Data capture:** CSV download or `/scrape-commsec`

---

## RACQ Bank

| DB Account Name          | Bank ID  | BSB     | Account No | Currency | Type     | Portal URL                                |
|--------------------------|----------|---------|------------|----------|----------|-------------------------------------------|
| Jacob RACQ Bonus Saver   | 10183440 | TODO    | 1830752    | AUD      | Savings  | https://banking.racq.com.au               |
| Jacob RACQ Everyday      | 10183440 | TODO    | 1830751    | AUD      | Everyday | https://banking.racq.com.au               |
| Darlene RACQ Everyday    | 10183440 | TODO    | TODO       | AUD      | Everyday | https://banking.racq.com.au               |

**Data capture:** `/scrape-racq`

---

## ANZ

| DB Account Name        | BSB     | Account No | Currency | Type     | Portal URL                                |
|------------------------|---------|------------|----------|----------|-------------------------------------------|
| Jacob ANZ Savings      | TODO    | TODO       | AUD      | Savings  | https://www.anz.com.au/ways-to-bank/internet-banking/ |
| Jacob ANZ Credit Card  | TODO    | TODO       | AUD      | Credit   | https://www.anz.com.au/ways-to-bank/internet-banking/ |

**Data capture:** Manual update (`towsand cash update`)

---

## Wise

| DB Account Name | Profile          | Currency | Type  | Portal URL                        |
|-----------------|------------------|----------|-------|-----------------------------------|
| Wise EUR        | jacob@lamorak.net | EUR      | Multi | https://wise.com/home             |
| Wise USD        | jacob@lamorak.net | USD      | Multi | https://wise.com/home             |
| Wise GBP        | jacob@lamorak.net | GBP      | Multi | https://wise.com/home             |

**Data capture:** `/scrape-wise`

---

## N26

| DB Account Name | IBAN        | Currency | Type     | Portal URL                        |
|-----------------|-------------|----------|----------|-----------------------------------|
| N26 Darlene     | TODO        | EUR      | Everyday | https://app.n26.com               |
| N26 Jacob       | TODO        | EUR      | Everyday | https://app.n26.com               |

**Data capture:** Manual update (`towsand cash update`)

---

## Other

| DB Account Name       | Identifier | Currency | Type       | Notes                          |
|-----------------------|------------|----------|------------|--------------------------------|
| Isepankur - Bondora   | TODO       | EUR      | P2P        | Below the line                 |
| Cash USD              | —          | USD      | Physical   | Below the line                 |
| Cash AUD              | —          | AUD      | Physical   | Below the line                 |
| Eroza Owed            | —          | AUD      | Receivable | Treatment TBD                  |

**Data capture:** Manual update (`towsand cash update`)
