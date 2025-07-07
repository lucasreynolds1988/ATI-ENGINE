// ~/Soap/frontend/src/AccountPage.js

import React from "react";
import ChangePassword from "./ChangePassword";

function AccountPage({ token }) {
  return (
    <div className="section-card">
      <h2>Account</h2>
      <ChangePassword token={token} />
    </div>
  );
}
export default AccountPage;
