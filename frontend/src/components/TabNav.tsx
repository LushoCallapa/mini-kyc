export type TabId = "register" | "registrations";

interface TabNavProps {
  activeTab: TabId;
  onChange: (tab: TabId) => void;
}

const TABS: { id: TabId; label: string }[] = [
  { id: "register", label: "New registration" },
  { id: "registrations", label: "Registered users" },
];

export default function TabNav({ activeTab, onChange }: TabNavProps) {
  return (
    <div className="tabs" role="tablist" aria-label="Sections">
      {TABS.map((tab) => (
        <button
          key={tab.id}
          id={`tab-${tab.id}`}
          type="button"
          role="tab"
          aria-selected={activeTab === tab.id}
          aria-controls={`panel-${tab.id}`}
          className={`tab ${activeTab === tab.id ? "is-active" : ""}`}
          onClick={() => onChange(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}