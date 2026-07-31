# Requirements: Overspend Warnings (`ALERT`)

Status: Shipped

- **ALERT-1.1** WHEN a category's month-to-date spend crosses 80% of its budget THE SYSTEM SHALL raise a local notification.
- **ALERT-1.2** WHEN the device is offline THE SYSTEM SHALL still evaluate and raise the warning from local data only.
- **ALERT-2.1** WHERE a user has set no budget for a category THE SYSTEM SHALL infer one from the trailing 3-month median.
- **ALERT-2.2** THE SYSTEM SHALL address the warning to the single owner of the ledger and to no other party.
