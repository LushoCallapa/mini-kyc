
import Navbar from "./components/Navbar";
import RegistrationForm from "./components/RegistrationForm";
import "./App.css";

export default function App() {
  return (
    <div className="app-shell">
      <Navbar />

      <main className="page">
        <RegistrationForm />
      </main>
    </div>
  );
}
