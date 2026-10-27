// Small reusable building blocks so every page looks the same.

export function Card({ title, children, className = "" }) {
  return (
    <section className={`rounded-2xl border border-slate-200 bg-white p-5 shadow-sm ${className}`}>
      {title && <h2 className="mb-4 text-lg font-semibold text-slate-900">{title}</h2>}
      {children}
    </section>
  );
}

export function Input({ label, ...props }) {
  return (
    <label className="block">
      {label && <span className="mb-1 block text-sm font-medium text-slate-700">{label}</span>}
      <input
        className="w-full rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
        {...props}
      />
    </label>
  );
}

export function Button({ children, variant = "primary", className = "", ...props }) {
  const styles = {
    primary: "bg-emerald-600 text-white hover:bg-emerald-700",
    secondary: "border border-slate-300 bg-white text-slate-700 hover:bg-slate-50",
    danger: "text-red-600 hover:bg-red-50",
  };
  return (
    <button
      className={`rounded-lg px-4 py-2 font-medium transition disabled:cursor-not-allowed disabled:opacity-50 ${styles[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

export function ErrorMessage({ children }) {
  if (!children) return null;
  return <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{children}</p>;
}

export function Spinner() {
  return <p className="py-10 text-center text-slate-500">Loading…</p>;
}
