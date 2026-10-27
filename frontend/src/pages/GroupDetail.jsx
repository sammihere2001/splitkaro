import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router";
import { useAuth } from "../auth.jsx";
import AddExpenseForm from "../components/AddExpenseForm.jsx";
import AddMemberForm from "../components/AddMemberForm.jsx";
import { Button, Card, ErrorMessage, Spinner } from "../components/ui.jsx";
import { formatDate, formatRs } from "../format.js";

export default function GroupDetail() {
  const { groupId } = useParams();
  const { request, user } = useAuth();
  const [data, setData] = useState(null); // { group, expenses, balances, settlements }
  const [error, setError] = useState("");

  // Loads everything on the page at once. Called again after any change.
  const reload = useCallback(async () => {
    try {
      const [group, expenses, balances, settlements] = await Promise.all([
        request(`/groups/${groupId}`),
        request(`/groups/${groupId}/expenses`),
        request(`/groups/${groupId}/balances`),
        request(`/groups/${groupId}/settle-up`),
      ]);
      setData({ group, expenses, balances, settlements });
      setError("");
    } catch (err) {
      setError(err.message);
    }
  }, [groupId, request]);

  useEffect(() => {
    reload();
  }, [reload]);

  async function deleteExpense(expense) {
    if (!window.confirm(`Delete "${expense.description}"?`)) return;
    try {
      await request(`/groups/${groupId}/expenses/${expense.id}`, { method: "DELETE" });
      await reload();
    } catch (err) {
      setError(err.message);
    }
  }

  if (!data) {
    return error ? <ErrorMessage>{error}</ErrorMessage> : <Spinner />;
  }

  const { group, expenses, balances, settlements } = data;
  const nameOf = (userId) => group.members.find((m) => m.id === userId)?.name ?? "Unknown";
  const canDelete = (expense) => user.id === expense.paid_by_id || user.id === group.created_by_id;

  return (
    <div className="space-y-6">
      <div>
        <Link to="/" className="text-sm text-emerald-700 hover:underline">
          ← All groups
        </Link>
        <h1 className="mt-1 text-2xl font-bold text-slate-900">{group.name}</h1>
      </div>

      <ErrorMessage>{error}</ErrorMessage>

      <div className="grid gap-6 md:grid-cols-2">
        <Card title="Balances">
          <ul className="divide-y divide-slate-100">
            {balances.map((b) => {
              const amount = Number(b.balance);
              return (
                <li key={b.user_id} className="flex justify-between py-2">
                  <span>{b.name}</span>
                  <span
                    className={
                      amount > 0 ? "font-medium text-emerald-600" : amount < 0 ? "font-medium text-red-600" : "text-slate-400"
                    }
                  >
                    {amount > 0 ? "gets back " : amount < 0 ? "owes " : ""}
                    {amount === 0 ? "settled" : formatRs(Math.abs(amount))}
                  </span>
                </li>
              );
            })}
          </ul>
        </Card>

        <Card title="Settle up">
          {settlements.length === 0 ? (
            <p className="text-slate-500">Everyone is settled 🎉</p>
          ) : (
            <ul className="space-y-2">
              {settlements.map((s, i) => (
                <li key={i} className="rounded-lg bg-slate-50 px-3 py-2">
                  <span className="font-medium">{nameOf(s.from_user_id)}</span> pays{" "}
                  <span className="font-medium">{nameOf(s.to_user_id)}</span>{" "}
                  <span className="font-semibold text-emerald-700">{formatRs(s.amount)}</span>
                </li>
              ))}
            </ul>
          )}
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card title="Add an expense">
          <AddExpenseForm groupId={groupId} onAdded={reload} />
        </Card>

        <Card title={`Members (${group.members.length})`}>
          <ul className="mb-4 flex flex-wrap gap-2">
            {group.members.map((m) => (
              <li key={m.id} className="rounded-full bg-emerald-50 px-3 py-1 text-sm text-emerald-800">
                {m.name}
              </li>
            ))}
          </ul>
          <AddMemberForm groupId={groupId} onAdded={reload} />
        </Card>
      </div>

      <Card title="Expenses">
        {expenses.length === 0 ? (
          <p className="text-slate-500">No expenses yet.</p>
        ) : (
          <ul className="divide-y divide-slate-100">
            {expenses.map((e) => (
              <li key={e.id} className="flex items-center justify-between gap-3 py-3">
                <div>
                  <p className="font-medium text-slate-900">{e.description}</p>
                  <p className="text-sm text-slate-500">
                    {nameOf(e.paid_by_id)} paid · split {e.shares.length} ways · {formatDate(e.created_at)}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-semibold">{formatRs(e.amount)}</span>
                  {canDelete(e) && (
                    <Button variant="danger" className="px-2 py-1 text-sm" onClick={() => deleteExpense(e)}>
                      Delete
                    </Button>
                  )}
                </div>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  );
}
