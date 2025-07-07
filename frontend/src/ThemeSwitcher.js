import React, { useState } from "react";

function ThemeSwitcher() {
  const [dark, setDark] = useState(true);

  const toggle = () => {
    document.body.classList.toggle("dark-theme", !dark);
    setDark(!dark);
  };

  return (
    <button
      onClick={toggle}
      className="absolute top-2 left-2 text-white text-sm bg-gray-700 px-3 py-1 rounded"
    >
      {dark ? "☀️ Light Mode" : "🌙 Dark Mode"}
    </button>
  );
}

export default ThemeSwitcher;
