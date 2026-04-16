import React, { useState } from 'react';
import { 
  Box, Button, Input, VStack, Heading, Text, Stack 
} from '@chakra-ui/react';
import { uploadDocument } from '../api';

const DocumentUpload = ({onUploadSuccess}) => {
  const [docName, setDocName] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!selectedFile || !docName) {
      alert("Please fill all fields");
      return;
    }

    setLoading(true);
    try {
      await uploadDocument(docName, selectedFile);
      if (onUploadSuccess) onUploadSuccess(); // Trigger the refresh!
      
      alert("Upload Successful! Your document has been sent for review.");
      setDocName('');
      setSelectedFile(null);
    } catch (error) {
      // Professional Error Handling: Pull the message from your Django 'Checker'
      const serverMessage = error.response?.data?.file?.[0] || "Upload failed";
      alert("Upload Error: " + serverMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box p={8} maxWidth="500px" borderWidth="1px" borderRadius="lg" boxShadow="md" m="auto" mt={10}>
      <VStack gap="6" align="stretch">
        <Heading size="md">Upload Internship Document</Heading>
        
        <Stack gap="2">
          <Text fontWeight="medium">Document Name</Text>
          <Input 
            placeholder="e.g. Acceptance Letter" 
            value={docName} 
            onChange={(e) => setDocName(e.target.value)} 
          />
        </Stack>

        <Stack gap="2">
          <Text fontWeight="medium">Select File (PDF only)</Text>
          <Input 
            type="file" 
            variant="outline"
            onChange={(e) => setSelectedFile(e.target.files[0])} 
          />
        </Stack>

        <Button 
          // In v3, colorScheme changed to colorPalette
          colorPalette="blue" 
          loading={loading} 
          onClick={handleUpload}
          width="full"
        >
          Submit to Portal
        </Button>
      </VStack>
    </Box>
  );
};

export default DocumentUpload;