import { useState } from "react";
import { useAuth } from "../auth.jsx";
import { Button, ErrorMessage, Input } from "./ui.jsx";

/** Form for adding a new expense, paid by you and split equally between all group members. */
export default function AddExpenseForm({ groupId, onAdded }) {
  const { request } = useAuth();
  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      await request(`/groups/${groupId}/expenses`, {
        method: "POST",
        body: { description, amount },
      });
      setDescription("");
      setAmount("");
      onAdded();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Description"
        placeholder="e.g. Electricity bill"
        required
        maxLength={200}
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <Input
        label="Amount (Rs)"
        type="number"
        min="0.01"
        step="0.01"
        placeholder="1500"
        required
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <p className="text-sm text-slate-500">You paid, split equally between everyone in the group.</p>
      <ErrorMessage>{error}</ErrorMessage>
      <Button type="submit" disabled={submitting} className="w-full">
        {submitting ? "Adding…" : "Add expense"}
      </Button>
    </form>
  );
}
