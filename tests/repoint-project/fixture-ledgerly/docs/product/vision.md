# Product Vision: Ledgerly

Status: Approved
Date: 2025-11-03

## Problem

People lose track of where their money goes. Bank apps show transactions but not
meaning — no categories that match how a person actually thinks about spending,
and no signal until the month is already over.

## Users

Individuals aged 25–40 managing personal money on a phone. They are not
accountants and will not learn double-entry bookkeeping.

## Goals

- **GOAL-1** A user can capture a receipt in under 10 seconds from lock screen.
- **GOAL-2** Spending is categorised automatically with no manual tagging.
- **GOAL-3** A user is warned before overspending a category, not after.
- **GOAL-4** The whole app works offline; sync is a convenience, never a requirement.

## Non-goals

- Multi-user accounts or shared ledgers.
- Tax filing, invoicing, or anything an accountant would recognise.
- Web app — mobile only.

## Scope boundaries

In scope now: iOS and Android, single user, one currency. Deferred: multi-currency.
Hard constraints: all financial data stays on-device unless the user opts into sync;
no third-party analytics SDKs.
