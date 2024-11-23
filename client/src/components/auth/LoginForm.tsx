import { useState } from 'react';
import {
  TextInput,
  PasswordInput,
  Button,
  Group,
  Stack,
  Text,
  Paper,
  Divider,
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { authService } from '../../services/authService';

interface LoginFormProps {
  onSuccess?: () => void;
  onRegisterClick?: () => void;
}

export function LoginForm({ onSuccess, onRegisterClick }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await authService.login({ email, password });
      notifications.show({
        title: 'Success',
        message: 'Logged in successfully',
        color: 'green',
      });
      onSuccess?.();
    } catch (error: any) {
      notifications.show({
        title: 'Error',
        message: error.message || 'Login failed',
        color: 'red',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper p="md" withBorder>
      <form onSubmit={handleSubmit}>
        <Stack spacing="md">
          <Text size="xl" weight={500}>
            Login
          </Text>

          <TextInput
            required
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.currentTarget.value)}
            placeholder="your.email@example.com"
          />

          <PasswordInput
            required
            label="Password"
            value={password}
            onChange={(e) => setPassword(e.currentTarget.value)}
            placeholder="Your password"
          />

          <Button type="submit" loading={loading}>
            Login
          </Button>

          <Divider />

          <Group position="apart" mt="xs">
            <Text size="sm">Don't have an account?</Text>
            <Button variant="subtle" onClick={onRegisterClick}>
              Register
            </Button>
          </Group>
        </Stack>
      </form>
    </Paper>
  );
}
