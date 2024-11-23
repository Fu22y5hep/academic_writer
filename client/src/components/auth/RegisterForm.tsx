import { useState } from 'react';
import { TextInput, PasswordInput, Button, Group, Box, Text } from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { authService } from '../../services/authService';

interface RegisterFormProps {
  onSuccess: () => void;
  onSwitchToLogin: () => void;
}

export function RegisterForm({ onSuccess, onSwitchToLogin }: RegisterFormProps) {
  const [loading, setLoading] = useState(false);

  const form = useForm({
    initialValues: {
      email: '',
      password: '',
      full_name: '',
    },
    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
      password: (value) => 
        value.length < 8 ? 'Password must be at least 8 characters' : null,
      full_name: (value) => 
        value.length < 2 ? 'Name must be at least 2 characters' : null,
    },
  });

  const handleSubmit = async (values: typeof form.values) => {
    try {
      setLoading(true);
      await authService.register({
        email: values.email,
        password: values.password,
        full_name: values.full_name,
      });
      notifications.show({
        title: 'Success',
        message: 'Registration successful! You are now logged in.',
        color: 'green',
      });
      onSuccess();
    } catch (error: any) {
      console.error('Registration error:', error);
      notifications.show({
        title: 'Error',
        message: error.message || 'Registration failed',
        color: 'red',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <form onSubmit={form.onSubmit(handleSubmit)}>
        <TextInput
          required
          label="Full Name"
          placeholder="John Doe"
          {...form.getInputProps('full_name')}
          mb="md"
        />
        <TextInput
          required
          label="Email"
          placeholder="your@email.com"
          {...form.getInputProps('email')}
          mb="md"
        />
        <PasswordInput
          required
          label="Password"
          placeholder="Your password"
          {...form.getInputProps('password')}
          mb="xl"
        />

        <Group justify="space-between">
          <Text size="sm">
            Already have an account?{' '}
            <Text
              component="span"
              color="blue"
              style={{ cursor: 'pointer' }}
              onClick={onSwitchToLogin}
            >
              Login
            </Text>
          </Text>
          <Button type="submit" loading={loading}>
            Register
          </Button>
        </Group>
      </form>
    </Box>
  );
}
