import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { useAuth } from "../auth.jsx";
import AuthCard from "../components/AuthCard.jsx";
import { Button, ErrorMessage, Input } from "../components/ui.jsx";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault(); // stop the browser from reloading the page
    setError("");
    setSubmitting(true);
    try {
      await login(email, password);
      navigate("/");
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AuthCard
      title="Welcome back"
      subtitle="Log in to see your groups"
      footer={
        <>
          New here?{" "}
          <Link to="/register" className="font-medium text-emerald-700 hover:underline">
            Create an account
          </Link>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input label="Email" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
        <Input
          label="Password"
          type="password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <ErrorMessage>{error}</ErrorMessage>
        <Button type="submit" disabled={submitting} className="w-full">
          {submitting ? "Logging in…" : "Log in"}
        </Button>
        {import.meta.env.PROD && (
          // The free hosting plan puts the server to sleep when nobody is using it.
          <p className="text-center text-xs text-slate-500">
            Demo on a free server: the first request can take up to a minute while it wakes up.
          </p>
        )}
      </form>
    </AuthCard>
  );
}
