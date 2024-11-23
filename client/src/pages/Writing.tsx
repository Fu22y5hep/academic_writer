import { Container, Title, Tabs, Paper, TextInput } from '@mantine/core';
import { useState } from 'react';
import { PlanningPanel } from '../components/writing/PlanningPanel';

export function Writing() {
  const [title, setTitle] = useState('');

  return (
    <Container size="lg" py="xl">
      <Title order={2} mb="xl">Writing Assistant</Title>

      <TextInput
        label="Document Title"
        placeholder="Enter document title"
        value={title}
        onChange={(event) => setTitle(event.currentTarget.value)}
        mb="lg"
      />

      <Tabs defaultValue="write">
        <Tabs.List>
          <Tabs.Tab value="write">Write</Tabs.Tab>
          <Tabs.Tab value="outline">Plan & Outline</Tabs.Tab>
          <Tabs.Tab value="suggestions">AI Suggestions</Tabs.Tab>
        </Tabs.List>

        <Paper p="md" mt="sm" withBorder>
          <Tabs.Panel value="write">
            <textarea
              style={{
                width: '100%',
                minHeight: '400px',
                padding: '1rem',
                border: '1px solid #e9ecef',
                borderRadius: '4px',
                resize: 'vertical',
                fontFamily: 'inherit',
              }}
              placeholder="Start writing here..."
            />
          </Tabs.Panel>

          <Tabs.Panel value="outline">
            <PlanningPanel />
          </Tabs.Panel>

          <Tabs.Panel value="suggestions">
            <p>AI suggestions will appear here as you write...</p>
          </Tabs.Panel>
        </Paper>
      </Tabs>
    </Container>
  );
}
