import { useRegistrations } from "../hooks/useRegistrations";
import { formatDateTime } from "../utils/formatDateTime";

export default function RegistrationsList() {
  const { records, isLoading, error, refresh } = useRegistrations();

  return (
    <section className="list-card" aria-labelledby="registrations-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">DIRECTORY</p>
          <h2 id="registrations-title">Registered users</h2>
        </div>

        <button
          type="button"
          className="refresh-button"
          onClick={refresh}
          disabled={isLoading}
        >
          {isLoading ? "Loading..." : "Refresh"}
        </button>
      </div>

      {error && (
        <div className="message error" role="alert">
          <strong>Unable to load registrations</strong>
          <p>{error}</p>
        </div>
      )}

      {!error && !isLoading && records.length === 0 && (
        <p className="empty-state">No registrations yet.</p>
      )}

      {records.length > 0 && (
        <div className="table-wrapper">
          <table className="records-table">
            <thead>
              <tr>
                <th scope="col">ID</th>
                <th scope="col">Full name</th>
                <th scope="col">Email</th>
                <th scope="col">Document</th>
                <th scope="col">Registered</th>
              </tr>
            </thead>

            <tbody>
              {records.map((record) => (
                <tr key={record.id}>
                  <td>{record.id}</td>
                  <td>{record.full_name}</td>
                  <td>{record.email}</td>
                  <td>{record.document_number}</td>
                  <td>{formatDateTime(record.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}