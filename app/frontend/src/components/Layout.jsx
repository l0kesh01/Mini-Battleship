import React from "react";
import TopBar from "./TopBar";

const Layout = ({ children }) => {
  return (
    <div className="app-root">
      <TopBar />
      <main className="app-main">{children}</main>
    </div>
  );
};

export default Layout;
