import { useState } from "react";

import Navbar from "./components/Navbar";
import RegistrationForm from "./components/RegistrationForm";
import RegistrationsList from "./components/RegistrationsList";
import TabNav, { type TabId } from "./components/TabNav";
import "./App.css";

export default function App() {
  const [activeTab, setActiveTab] = useState<TabId>("register");

  return (
    <div className="app-shell">
      <Navbar />

      <main className="page">
        <TabNav activeTab={activeTab} onChange={setActiveTab} />

        <div
          role="tabpanel"
          id="panel-register"
          aria-labelledby="tab-register"
          hidden={activeTab !== "register"}
        >
          <RegistrationForm />
        </div>

        {activeTab === "registrations" && (
          <div
            role="tabpanel"
            id="panel-registrations"
            aria-labelledby="tab-registrations"
          >
            <RegistrationsList />
          </div>
        )}
      </main>
    </div>
  );
}