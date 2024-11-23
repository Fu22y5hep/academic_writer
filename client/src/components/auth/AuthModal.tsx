import { useState } from 'react';
import { Modal } from '@mantine/core';
import { LoginForm } from './LoginForm';
import { RegisterForm } from './RegisterForm';

interface AuthModalProps {
  opened: boolean;
  onClose: () => void;
}

export function AuthModal({ opened, onClose }: AuthModalProps) {
  const [isLogin, setIsLogin] = useState(true);

  const handleSuccess = () => {
    onClose();
  };

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title={isLogin ? 'Login' : 'Register'}
      size="sm"
    >
      {isLogin ? (
        <LoginForm
          onSuccess={handleSuccess}
          onRegisterClick={() => setIsLogin(false)}
        />
      ) : (
        <RegisterForm
          onSuccess={handleSuccess}
          onLoginClick={() => setIsLogin(true)}
        />
      )}
    </Modal>
  );
}
