export default function Navbar() {
  return (
    <nav className="navbar" aria-label="Main navigation">
      <a className="brand" href="/" aria-label="Fractal Mini KYC home">
        <span className="brand-mark" aria-hidden="true">
          F
        </span>

        <span className="brand-copy">
          <strong>FRACTAL</strong>
          <span>Digital onboarding</span>
        </span>
      </a>

      <div className="navbar-status">
        <span className="status-dot" aria-hidden="true" />
        <span>Identity verification</span>
      </div>
    </nav>
  );
}
