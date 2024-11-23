import { NavLink } from '@mantine/core';
import { IconHome2, IconPencil, IconBooks, IconBrain, IconSettings } from '@tabler/icons-react';
import { useLocation, useNavigate } from 'react-router-dom';

interface NavItem {
  icon: typeof IconHome2;
  label: string;
  path: string;
}

const navItems: NavItem[] = [
  { icon: IconHome2, label: 'Dashboard', path: '/' },
  { icon: IconPencil, label: 'Writing', path: '/writing' },
  { icon: IconBooks, label: 'Citations', path: '/citations' },
  { icon: IconBrain, label: 'AI Assistant', path: '/assistant' },
  { icon: IconSettings, label: 'Settings', path: '/settings' },
];

export function MainNavigation() {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <nav>
      {navItems.map((item) => (
        <NavLink
          key={item.label}
          active={location.pathname === item.path}
          label={item.label}
          leftSection={<item.icon size="1.2rem" stroke={1.5} />}
          onClick={() => navigate(item.path)}
        />
      ))}
    </nav>
  );
}
