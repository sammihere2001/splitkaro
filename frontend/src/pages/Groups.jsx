import { useEffect, useState } from "react";
import { Link } from "react-router";
import { useAuth } from "../auth.jsx";
import { Button, Card, ErrorMessage, Input, Spinner } from "../components/ui.jsx";

export default function Groups() {
  const { request } = useAuth();
  const [groups, setGroups] = useState(null); // null = still loading
  const [error, setError] = useState("");
  const [newName, setNewName] = useState("");
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    request("/groups")
      .then(setGroups)
      .catch((err) => setError(err.message));
  }, [request]);

  async function createGroup(event) {
    event.preventDefault();
    setError("");
    setCreating(true);
    try {
      const group = await request("/groups", { method: "POST", body: { name: newName } });
      setGroups((current) => [group, ...current]);
      setNewName("");
    } catch (err) {
      setError(err.message);
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Your groups</h1>

      <Card>
        <form onSubmit={createGroup} className="flex flex-col gap-3 sm:flex-row sm:items-end">
          <div className="flex-1">
            <Input
              label="New group"
              placeholder="e.g. Flat 4B, Murree trip"
              required
              maxLength={100}
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
            />
          </div>
          <Button type="submit" disabled={creating}>
            {creating ? "Creating…" : "Create group"}
          </Button>
        </form>
      </Card>

      <ErrorMessage>{error}</ErrorMessage>

      {groups === null && !error && <Spinner />}

      {groups?.length === 0 && (
        <p className="py-10 text-center text-slate-500">No groups yet. Create one above to get started.</p>
      )}

      <div className="grid gap-4 sm:grid-cols-2">
        {groups?.map((group) => (
          <Link
            key={group.id}
            to={`/groups/${group.id}`}
            className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-emerald-400 hover:shadow"
          >
            <h2 className="text-lg font-semibold text-slate-900">{group.name}</h2>
            <p className="mt-1 text-sm text-slate-500">
              {group.members.length} {group.members.length === 1 ? "member" : "members"} ·{" "}
              {group.members.map((m) => m.name).join(", ")}
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}
