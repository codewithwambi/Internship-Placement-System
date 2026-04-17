import React, { useState } from 'react';
import { 
  Box, Button, Input, Heading, VStack, Stack, Text, Link 
} from '@chakra-ui/react';
import api from '../api';

const Login = ({ onAuthSuccess }) => {
  const [mode, setMode] = useState('login'); // 'login' or 'register'
  const [loading, setLoading] = useState(false);
  
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '',
    first_name: '',
    last_name: '',
    registration_number: '',
    course: '',
    role: 'STUDENT'
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    // Choose endpoint based on mode
    const endpoint = mode === 'login' ? 'token/' : 'register/';
    
    // Professional Tip: Only send what the backend expects
    const payload = mode === 'login' 
      ? { username: formData.username, password: formData.password }
      : formData;

    try {
      const response = await api.post(endpoint, payload);
      
      // Extract tokens and user info based on response structure
      const tokens = mode === 'login' ? response.data : response.data.tokens;
      const userDetails = mode === 'login' ? response.data : response.data.user;

      // Single hand-off to App.jsx
      onAuthSuccess({
        token: tokens.access,
        username: userDetails.username || formData.username,
        role: userDetails.role || formData.role
      });

    } catch (error) {
      console.error("Auth Error:", error.response?.data);
      
      // Deep extraction of Django error messages
      const serverError = error.response?.data;
      let errorMessage = "An error occurred during authentication.";

      if (serverError?.detail) {
        errorMessage = serverError.detail;
      } else if (typeof serverError === 'object') {
        // Grab the first validation error found (e.g., "username already exists")
        const firstKey = Object.keys(serverError)[0];
        errorMessage = `${firstKey}: ${serverError[firstKey][0]}`;
      }
      
      alert(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box maxW="md" mx="auto" mt={10} p={8} borderWidth="1px" borderRadius="xl" boxShadow="lg" bg="white">
      <VStack gap={6} align="stretch">
        <Box textAlign="center">
          <Heading size="lg">{mode === 'login' ? 'Welcome Back' : 'Join the IPS'}</Heading>
          <Text color="gray.500" fontSize="sm">
            {mode === 'login' ? 'Makerere University Portal' : 'Create your student account'}
          </Text>
        </Box>

        <form onSubmit={handleSubmit}>
          <Stack gap={3}>
            {mode === 'register' && (
              <>
                <Stack direction="row" gap={2}>
                  <Input placeholder="First Name" name="first_name" onChange={handleChange} required />
                  <Input placeholder="Last Name" name="last_name" onChange={handleChange} required />
                </Stack>
                <Input placeholder="Email" type="email" name="email" onChange={handleChange} required />
                <Input placeholder="Registration Number" name="registration_number" onChange={handleChange} required />
                <Input placeholder="Course (e.g. BSSE)" name="course" onChange={handleChange} required />
              </>
            )}

            <Input placeholder="Username" name="username" onChange={handleChange} required />
            <Input placeholder="Password" type="password" name="password" onChange={handleChange} required />

            <Button 
              type="submit" 
              colorPalette="blue" 
              loading={loading} 
              mt={4}
              width="full"
            >
              {mode === 'login' ? 'Sign In' : 'Create Account'}
            </Button>
          </Stack>
        </form>

        <Box textAlign="center">
          <Text fontSize="sm">
            {mode === 'login' ? "Don't have an account?" : "Already have an account?"}{' '}
            <Link 
              color="blue.500" 
              fontWeight="bold" 
              onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
            >
              {mode === 'login' ? 'Register here' : 'Login here'}
            </Link>
          </Text>
        </Box>
      </VStack>
    </Box>
  );
};

export default Login;