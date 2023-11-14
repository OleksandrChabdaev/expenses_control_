import { BrowserRouter } from "react-router-dom";
import { GoogleOAuthProvider } from "@react-oauth/google";
import "bootstrap/dist/css/bootstrap.min.css";
import ExpensesPage from "./pages/ExpensesPage";

function App() {
  return (
    <GoogleOAuthProvider clientId="1088538144022-ihglr48dvv901c171jc495f509d8059o.apps.googleusercontent.com">
      <BrowserRouter>
        <ExpensesPage />
      </BrowserRouter>
    </GoogleOAuthProvider>
  );
}

export default App;
