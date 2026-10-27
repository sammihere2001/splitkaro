import { Link } from "react-router";

/** The centred box used by both the login and register pages. */
export default function AuthCard({ title, subtitle, children, footer }) {
  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <Link to="/" className="mb-6 block text-center text-3xl font-bold text-emerald-700">
          SplitKaro
        </Link>
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h1 className="text-xl font-semibold text-slate-900">{title}</h1>
          <p className="mb-5 text-sm text-slate-500">{subtitle}</p>
          {children}
        </div>
        <p className="mt-4 text-center text-sm text-slate-600">{footer}</p>
      </div>
    </div>
  );
}
