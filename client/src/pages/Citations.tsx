import { Container, Title, Select, Table, ActionIcon, Group, Button } from '@mantine/core';
import { IconTrash, IconEdit } from '@tabler/icons-react';

export function Citations() {
  const citations = [
    { id: 1, author: 'Smith, J.', title: 'Example Paper Title', year: 2023, journal: 'Journal of Examples' },
    { id: 2, author: 'Johnson, A.', title: 'Another Research Paper', year: 2022, journal: 'Science Today' },
  ];

  return (
    <Container size="lg" py="xl">
      <Group justify="space-between" mb="xl">
        <Title order={2}>Citations Manager</Title>
        <Group>
          <Select
            data={['APA', 'MLA', 'Chicago', 'Harvard']}
            defaultValue="APA"
            label="Citation Style"
          />
          <Button>Add Citation</Button>
        </Group>
      </Group>

      <Table>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Author</Table.Th>
            <Table.Th>Title</Table.Th>
            <Table.Th>Year</Table.Th>
            <Table.Th>Journal</Table.Th>
            <Table.Th>Actions</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {citations.map((citation) => (
            <Table.Tr key={citation.id}>
              <Table.Td>{citation.author}</Table.Td>
              <Table.Td>{citation.title}</Table.Td>
              <Table.Td>{citation.year}</Table.Td>
              <Table.Td>{citation.journal}</Table.Td>
              <Table.Td>
                <Group gap="xs">
                  <ActionIcon variant="subtle" color="blue">
                    <IconEdit size="1rem" />
                  </ActionIcon>
                  <ActionIcon variant="subtle" color="red">
                    <IconTrash size="1rem" />
                  </ActionIcon>
                </Group>
              </Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>
    </Container>
  );
}
