// The API sends money as strings like "1500.00" so no precision is lost in JSON.
export function formatRs(amount) {
  const value = Number(amount).toLocaleString("en-PK", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  return `Rs ${value}`;
}

export function formatDate(isoString) {
  return new Date(isoString).toLocaleDateString("en-PK", { day: "numeric", month: "short", year: "numeric" });
}
