function escapeCsvCell(value: string | number | boolean | null): string {
  if (value === null) return "";
  // Keep genuinely numeric values intact; protect untrusted text cells in spreadsheet apps.
  const raw = String(value);
  const text = typeof value === "string" && /^[\\s\\u0000-\\u001f]*[=+\\-@]/u.test(raw)
    ? `\'${raw}`
    : raw;
  return /[",\r\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

export function exportToCSV(
  columns: string[],
  rows: (string | number | boolean | null)[][],
  filename: string
): void {
  const csv = [columns, ...rows]
    .map((row) => row.map(escapeCsvCell).join(","))
    .join("\r\n");
  const blob = new Blob(["\uFEFF", csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}
