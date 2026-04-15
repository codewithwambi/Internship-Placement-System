import React from 'react';
import { 
  ChakraProvider, 
  createSystem, 
  defaultConfig,
  Container, 
  Box, 
  Flex, 
  Heading, 
  Spacer, 
  Text 
} from '@chakra-ui/react';
import DocumentUpload from './components/DocumentUpload';

// This 'system' is what v3 needs to stop the 'disableLayers' error
const system = createSystem(defaultConfig);

function App() {
  return (
    <ChakraProvider value={system}>
      {/* Navigation Bar */}
      <Box bg="blue.700" px={4} py={3} color="white">
        <Flex minWidth="max-content" alignItems="center" gap="2">
          <Box p="2">
            <Heading size="md">IPS Manager</Heading>
          </Box>
          <Spacer />
          <Text fontSize="sm" fontWeight="bold">Wambi Elvis | Student Portal</Text>
        </Flex>
      </Box>

      {/* Main Content Area */}
      <Container maxW="container.xl" py={10}>
        <Flex direction="column" align="center">
          <Heading mb={2} size="xl" textAlign="center">
            Internship Placement System
          </Heading>
          <Text mb={8} color="gray.600">
            Submit and track your internship documentation for verification.
          </Text>

          {/* Our Upload Component */}
          <DocumentUpload />
        </Flex>
      </Container>
    </ChakraProvider>
  );
}

export default App;