import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "./components/layout/AppShell";
import { CapturePage } from "./pages/CapturePage";
import { DashboardPage } from "./pages/DashboardPage";
import { HistoryPage } from "./pages/HistoryPage";
import { NewInspectionPage } from "./pages/NewInspectionPage";
import { ProcessingPage } from "./pages/ProcessingPage";
import { ResultPage } from "./pages/ResultPage";

export default function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route element={<Navigate replace to="/dashboard" />} index />
        <Route element={<DashboardPage />} path="/dashboard" />
        <Route element={<NewInspectionPage />} path="/inspection/new" />
        <Route element={<CapturePage />} path="/inspection/:id/capture" />
        <Route element={<ProcessingPage />} path="/inspection/:id/processing" />
        <Route element={<ResultPage />} path="/inspection/:id" />
        <Route element={<HistoryPage />} path="/inspections" />
      </Route>
      <Route element={<Navigate replace to="/dashboard" />} path="*" />
    </Routes>
  );
}
