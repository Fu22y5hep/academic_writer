import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Divider,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Edit as EditIcon,
  FormatQuote as CitationsIcon,
  Chat as AssistantIcon,
  Settings as SettingsIcon,
  Assignment as PlanningIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const drawerWidth = 240;

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
  { text: 'Writing', icon: <EditIcon />, path: '/writing' },
  { text: 'Essay Plans', icon: <PlanningIcon />, path: '/essay-plans' },
  { text: 'Citations', icon: <CitationsIcon />, path: '/citations' },
  { text: 'Assistant', icon: <AssistantIcon />, path: '/assistant' },
  { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
];

export const Navigation: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}
    >
      <List sx={{ mt: 8 }}>
        {menuItems.map((item, index) => (
          <React.Fragment key={item.text}>
            {index === 5 && <Divider sx={{ my: 1 }} />}
            <ListItem disablePadding>
              <ListItemButton
                selected={location.pathname === item.path}
                onClick={() => navigate(item.path)}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </ListItem>
          </React.Fragment>
        ))}
      </List>
    </Drawer>
  );
};
