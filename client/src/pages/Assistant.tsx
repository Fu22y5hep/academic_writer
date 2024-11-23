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
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: messages.length + 1,
      role: 'user',
      content: input,
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/test/test-openai', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });

      if (!response.ok) {
        throw new Error('Failed to get AI response');
      }

      const data = await response.json();
      
      const aiMessage: Message = {
        id: messages.length + 2,
        role: 'assistant',
        content: data.response || 'Sorry, I encountered an error processing your request.',
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage: Message = {
        id: messages.length + 2,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
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
              disabled={isLoading}
            />
            <Button type="submit" loading={isLoading}>Send</Button>
          </div>
        </form>
      </Paper>
    </Container>
  );
}
