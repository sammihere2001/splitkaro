import { useState } from "react";
import { useAuth } from "../auth.jsx";
import { Button, ErrorMessage, Input } from "./ui.jsx";

export default function AddMemberForm({ groupId, onAdded }) {
  const { request } = useAuth();
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await request(`/groups/${groupId}/members`, { method: "POST", body: { email } });
      setEmail("");
      onAdded();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-2">
      <div className="flex gap-2">
        <div className="flex-1">
          <Input
            type="email"
            placeholder="friend@example.com"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <Button type="submit" variant="secondary" disabled={submitting}>
          Add
        </Button>
      </div>
      <ErrorMessage>{error}</ErrorMessage>
    </form>
  );
}
