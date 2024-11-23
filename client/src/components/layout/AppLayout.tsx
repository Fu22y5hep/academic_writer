import { AppShell, Burger, Group, Text } from '@mantine/core';
import { useState } from 'react';
import { MainNavigation } from './MainNavigation';
import { Routes } from '../../routes';

export function AppLayout() {
  const [opened, setOpened] = useState(false);

  return (
    <AppShell
      header={{ height: 60 }}
      navbar={{
        width: 300,
        breakpoint: 'sm',
        collapsed: { desktop: false, mobile: !opened }
      }}
      padding="md"
    >
      <AppShell.Header>
        <Group h="100%" px="md">
          <Burger
            opened={opened}
            onClick={() => setOpened(!opened)}
            hiddenFrom="sm"
            size="sm"
          />
          <Text size="lg" fw={700}>Academic Writing Assistant</Text>
        </Group>
      </AppShell.Header>

      <AppShell.Navbar p="md">
        <MainNavigation />
      </AppShell.Navbar>

      <AppShell.Main>
        <Routes />
      </AppShell.Main>
    </AppShell>
  );
}
