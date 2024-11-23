import { Container, Title, Paper, Switch, Select, Stack, Text } from '@mantine/core';
import { useState } from 'react';

export function Settings() {
  const [darkMode, setDarkMode] = useState(false);
  const [language, setLanguage] = useState('en');
  const [citationStyle, setCitationStyle] = useState('apa');
  const [notifications, setNotifications] = useState(true);

  return (
    <Container size="lg" py="xl">
      <Title order={2} mb="xl">Settings</Title>

      <Paper withBorder p="xl">
        <Stack spacing="xl">
          <div>
            <Text fw={500} mb="xs">Theme</Text>
            <Switch
              label="Dark mode"
              checked={darkMode}
              onChange={(event) => setDarkMode(event.currentTarget.checked)}
            />
          </div>

          <div>
            <Text fw={500} mb="xs">Language</Text>
            <Select
              value={language}
              onChange={(value) => setLanguage(value || 'en')}
              data={[
                { value: 'en', label: 'English' },
                { value: 'es', label: 'Spanish' },
                { value: 'fr', label: 'French' },
                { value: 'de', label: 'German' },
              ]}
            />
          </div>

          <div>
            <Text fw={500} mb="xs">Default Citation Style</Text>
            <Select
              value={citationStyle}
              onChange={(value) => setCitationStyle(value || 'apa')}
              data={[
                { value: 'apa', label: 'APA' },
                { value: 'mla', label: 'MLA' },
                { value: 'chicago', label: 'Chicago' },
                { value: 'harvard', label: 'Harvard' },
              ]}
            />
          </div>

          <div>
            <Text fw={500} mb="xs">Notifications</Text>
            <Switch
              label="Enable notifications"
              checked={notifications}
              onChange={(event) => setNotifications(event.currentTarget.checked)}
            />
          </div>
        </Stack>
      </Paper>
    </Container>
  );
}
