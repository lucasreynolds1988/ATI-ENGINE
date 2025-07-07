export default function detectFileType(filename) {
  const ext = filename.split('.').pop().toLowerCase();
  if (["pdf", "docx", "txt"].includes(ext)) return ext;
  return "unknown";
}
