import React, { useEffect, useState } from 'react';
import { 
  Box, 
  Grid, 
  GridItem, 
  Heading, 
  Text, 
  VStack, 
  Stack,
  Badge, 
  Flex
} from '@chakra-ui/react';
import DocumentUpload from './DocumentUpload';
import api from '../api';

const StudentDashboard = () => {
  const [documents, setDocuments] = useState([]);

  const fetchMyDocuments = async () => {
    try {
      const response = await api.get('documents/'); 
      setDocuments(response.data);
    } catch (error) {
      console.error("Error fetching documents:", error);
    }
  };

  useEffect(() => {
    fetchMyDocuments();
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'APPROVED': return 'green';
      case 'REJECTED': return 'red';
      default: return 'yellow';
    }
  };

  return (
    <Box p={8}>
      <VStack align="start" gap={2} mb={10}>
        <Heading size="2xl">Welcome, Wambi Elvis</Heading>
        <Text fontSize="lg" color="gray.600">
          Makerere University Internship Placement System
        </Text>
      </VStack>

      {/* Using a standard Grid which is very stable in v3 */}
      <Grid templateColumns={{ base: "1fr", lg: "1fr 1fr" }} gap={10}>
        
        <GridItem>
          <Box p={6} borderWidth="1px" borderRadius="lg" bg="white">
            <Heading size="md" mb={6}>Submit New Document</Heading>
            <DocumentUpload onUploadSuccess={fetchMyDocuments} />
          </Box>
        </GridItem>

        <GridItem>
          <Box p={6} borderWidth="1px" borderRadius="lg" bg="white">
            <Heading size="md" mb={6}>My Submissions</Heading>
            
            {documents.length === 0 ? (
              <Text color="gray.400">No documents submitted yet.</Text>
            ) : (
              <Stack gap={4}>
                {documents.map((doc) => (
                  <Box key={doc.id} p={4} borderWidth="1px" borderRadius="md">
                    <Flex justify="space-between" align="center">
                      <Box>
                        <Text fontWeight="bold">{doc.document_name}</Text>
                        <Text fontSize="xs" color="gray.500">
                          {new Date(doc.uploaded_at).toLocaleDateString()}
                        </Text>
                      </Box>
                      <Badge colorPalette={getStatusColor(doc.status)}>
                        {doc.status}
                      </Badge>
                    </Flex>
                  </Box>
                ))}
              </Stack>
            )}
          </Box>
        </GridItem>

      </Grid>
    </Box>
  );
};

export default StudentDashboard;