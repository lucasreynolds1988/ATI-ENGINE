import { useState } from "react";

export default function useFileReader() {
  const [content, setContent] = useState("");

  const readFile = (file) => {
    const reader = new FileReader();
    reader.onload = () => setContent(reader.result);
    reader.readAsText(file);
  };

  return [content, readFile];
}
