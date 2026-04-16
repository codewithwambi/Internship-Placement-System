import React, { useState } from 'react';
import { 
  Box, Button, Input, VStack, Heading, Stack,Text, Field, Container 
} from '@chakra-ui/react';
import { loginUser } from '../api';

const Login = (onLoginSuccess) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
  e.preventDefault();
  try {
    const data = await loginUser(username, password);
    localStorage.setItem('username',data.username);
    onLoginSuccess(data);
    
    // Check the role we added to the Serializer
    if (data.role === 'STUDENT') {
      window.location.href = '/student-dashboard';
    } else if (data.role === 'ACADEMIC_SUPERVISOR' || data.role === 'WORKPLACE_SUPERVISOR') {
      window.location.href = '/supervisor-dashboard';
    } else if (data.role === 'ADMIN') {
      window.location.href = '/admin-panel';
    }
  } catch (error) {
    alert("Invalid credentials. Please try again.");
  }
};
   

  return (
    <Container maxW="sm" centerContent mt={20}>
      <Box p={8} borderWidth="1px" borderRadius="lg" boxShadow="xl" width="full" bg="white">
        <VStack gap={6}>
          <Heading size="lg">IPS Login</Heading>
          <Text color="gray.500" fontSize="sm">Makerere University Portal</Text>
          
          <Stack gap={4} width="full">
            <Input 
              placeholder="Username" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
            />
            <Input 
              placeholder="Password" 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
            />
            <Button 
              colorPalette="blue" 
              width="full" 
              loading={loading} 
              onClick={handleLogin}
            >
              Sign In
            </Button>
          </Stack>
        </VStack>
      </Box>
    </Container>
  );
};

export default Login;