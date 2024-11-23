import { Container, Title, Paper, TextInput, Button, Stack, Text } from '@mantine/core';
import { useState } from 'react';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
}

export function Assistant() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      role: 'assistant',
      content: 'Hello! I\'m your academic writing assistant. How can I help you today?',
    },
  ]);
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessage: Message = {
      id: messages.length + 1,
      role: 'user',
      content: input,
    };

    setMessages([...messages, newMessage]);
    setInput('');

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: Message = {
        id: messages.length + 2,
        role: 'assistant',
        content: 'I understand your query. Let me help you with that...',
      };
      setMessages((prev) => [...prev, aiResponse]);
    }, 1000);
  };

  return (
    <Container size="lg" py="xl">
      <Title order={2} mb="xl">AI Assistant</Title>

      <Paper withBorder p="md" style={{ height: 'calc(100vh - 200px)', display: 'flex', flexDirection: 'column' }}>
        <Stack
          spacing="md"
          style={{
            flex: 1,
            overflowY: 'auto',
            padding: '1rem',
          }}
        >
          {messages.map((message) => (
            <Paper
              key={message.id}
              p="sm"
              bg={message.role === 'assistant' ? 'blue.0' : 'gray.0'}
              style={{
                maxWidth: '80%',
                marginLeft: message.role === 'assistant' ? 0 : 'auto',
                marginRight: message.role === 'assistant' ? 'auto' : 0,
              }}
            >
              <Text size="sm">{message.content}</Text>
            </Paper>
          ))}
        </Stack>

        <form onSubmit={handleSubmit}>
          <div style={{ display: 'flex', gap: '0.5rem', padding: '1rem' }}>
            <TextInput
              placeholder="Type your message..."
              value={input}
              onChange={(e) => setInput(e.currentTarget.value)}
              style={{ flex: 1 }}
            />
            <Button type="submit">Send</Button>
          </div>
        </form>
      </Paper>
    </Container>
  );
}
