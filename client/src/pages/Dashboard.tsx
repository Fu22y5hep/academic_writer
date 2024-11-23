import { Container, Title, SimpleGrid, Paper, Text, Button, Group } from '@mantine/core';
import { IconPencil, IconBooks, IconBrain } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';

export function Dashboard() {
  const navigate = useNavigate();

  const features = [
    {
      icon: IconPencil,
      title: 'Writing Assistant',
      description: 'Get help with academic writing, structure, and style',
      path: '/writing',
    },
    {
      icon: IconBooks,
      title: 'Citation Manager',
      description: 'Manage and format your citations and references',
      path: '/citations',
    },
    {
      icon: IconBrain,
      title: 'AI Assistant',
      description: 'Get intelligent suggestions and feedback',
      path: '/assistant',
    },
  ];

  return (
    <Container size="lg" py="xl">
      <Title order={2} mb="xl">Welcome to Academic Writing Assistant</Title>

      <SimpleGrid cols={{ base: 1, sm: 2, md: 3 }} spacing="lg">
        {features.map((feature) => (
          <Paper key={feature.title} p="xl" radius="md" withBorder>
            <feature.icon size={32} stroke={1.5} />
            <Text size="lg" fw={500} mt="md">
              {feature.title}
            </Text>
            <Text size="sm" c="dimmed" mt="sm">
              {feature.description}
            </Text>
            <Group mt="md">
              <Button variant="light" onClick={() => navigate(feature.path)}>
                Get Started
              </Button>
            </Group>
          </Paper>
        ))}
      </SimpleGrid>
    </Container>
  );
}
