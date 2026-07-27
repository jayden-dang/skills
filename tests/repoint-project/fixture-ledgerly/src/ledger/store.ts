import { db } from "../db/sqlite";

// ARCH-1: local-first. Every write lands here before the sync layer sees it.
// ARCH-3: rows are single-owner — there is deliberately no tenant/org column.
export interface LedgerRow {
  id: string;
  occurredAt: number;
  amountMinor: number;
  categoryId: string;
  merchantRaw: string;
  note: string | null;
}

export async function appendRow(row: LedgerRow): Promise<void> {
  await db.run(
    `INSERT INTO ledger (id, occurred_at, amount_minor, category_id, merchant_raw, note)
     VALUES (?, ?, ?, ?, ?, ?)`,
    [row.id, row.occurredAt, row.amountMinor, row.categoryId, row.merchantRaw, row.note],
  );
  await enqueueForSync(row.id);
}

export async function rowsInMonth(year: number, month: number): Promise<LedgerRow[]> {
  const [from, to] = monthBounds(year, month);
  return db.all(`SELECT * FROM ledger WHERE occurred_at >= ? AND occurred_at < ?`, [from, to]);
}
