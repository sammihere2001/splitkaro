import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { useAuth } from "../auth.jsx";
import AuthCard from "../components/AuthCard.jsx";
import { Button, ErrorMessage, Input } from "../components/ui.jsx";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await register(name, email, password);
      navigate("/");
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AuthCard
      title="Create your account"
      subtitle="Start splitting expenses with your friends"
      footer={
        <>
          Already have an account?{" "}
          <Link to="/login" className="font-medium text-emerald-700 hover:underline">
            Log in
          </Link>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input label="Name" required maxLength={100} value={name} onChange={(e) => setName(e.target.value)} />
        <Input label="Email" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
        <Input
          label="Password"
          type="password"
          required
          minLength={8}
          maxLength={72}
          placeholder="At least 8 characters"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <ErrorMessage>{error}</ErrorMessage>
        <Button type="submit" disabled={submitting} className="w-full">
          {submitting ? "Creating account…" : "Sign up"}
        </Button>
      </form>
    </AuthCard>
  );
}
