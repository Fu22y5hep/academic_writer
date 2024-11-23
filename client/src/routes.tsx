import { Routes as RouterRoutes, Route } from 'react-router-dom';
import { Dashboard } from './pages/Dashboard';
import { Writing } from './pages/Writing';
import { Citations } from './pages/Citations';
import { Assistant } from './pages/Assistant';
import { Settings } from './pages/Settings';

export function Routes() {
  return (
    <RouterRoutes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/writing" element={<Writing />} />
      <Route path="/citations" element={<Citations />} />
      <Route path="/assistant" element={<Assistant />} />
      <Route path="/settings" element={<Settings />} />
    </RouterRoutes>
  );
}
