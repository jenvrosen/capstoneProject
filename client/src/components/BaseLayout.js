import React from "react";
import { Link } from "react-router-dom";

const BaseLayout = ({ children, hideNavigation }) => (
  <div>
    <header>
      <div className="app-name">AI Advisor</div>
      <nav className="navbar">
        {!hideNavigation && (
          <ul>
            <li>
              <Link to="/admin_page">Administrator</Link>
            </li>
            <li>
              <Link to="/home">Home</Link>
            </li>
            <li>
              <Link to="/myprofile">My Profile</Link>
            </li>
            <li>
              <Link to="/signout">Sign Out</Link>
            </li>
          </ul>
        )}
      </nav>
    </header>
    <main>{children}</main>
  </div>
);

export default BaseLayout;
