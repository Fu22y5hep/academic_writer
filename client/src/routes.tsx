import { Routes as RouterRoutes, Route } from 'react-router-dom';
import { Dashboard } from './pages/Dashboard';
import { Writing } from './pages/Writing';
import { Citations } from './pages/Citations';
import { Assistant } from './pages/Assistant';
import { Settings } from './pages/Settings';
import { EssayPlanList } from './components/essay-planning/EssayPlanList';
import { EssayPlanForm } from './components/essay-planning/EssayPlanForm';

export function Routes() {
  const routes = [
    {
      path: '/',
      element: <Dashboard />,
    },
    {
      path: '/writing',
      element: <Writing />,
    },
    {
      path: '/citations',
      element: <Citations />,
    },
    {
      path: '/assistant',
      element: <Assistant />,
    },
    {
      path: '/settings',
      element: <Settings />,
    },
    {
      path: '/essay-plans',
      element: <EssayPlanList />,
    },
    {
      path: '/essay-plans/new',
      element: <EssayPlanForm />,
    },
    {
      path: '/essay-plans/:id/edit',
      element: <EssayPlanForm />,
    },
  ];

  return (
    <RouterRoutes>
      {routes.map((route) => (
        <Route key={route.path} path={route.path} element={route.element} />
      ))}
    </RouterRoutes>
  );
}
