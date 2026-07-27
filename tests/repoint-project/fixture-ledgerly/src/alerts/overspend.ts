import { rowsInMonth } from "../ledger/store";
import { notifyLocal } from "../platform/notifications";

// ALERT-1.1 / ALERT-2.2 — single-owner warning, evaluated from local rows only.
export async function checkOverspend(year: number, month: number, budgets: Map<string, number>) {
  const rows = await rowsInMonth(year, month);
  const byCategory = new Map<string, number>();
  for (const r of rows) {
    byCategory.set(r.categoryId, (byCategory.get(r.categoryId) ?? 0) + r.amountMinor);
  }
  for (const [categoryId, spent] of byCategory) {
    const budget = budgets.get(categoryId) ?? inferBudget(categoryId);
    if (spent >= budget * 0.8) {
      await notifyLocal(`You're at ${Math.round((spent / budget) * 100)}% of ${categoryId}`);
    }
  }
}
