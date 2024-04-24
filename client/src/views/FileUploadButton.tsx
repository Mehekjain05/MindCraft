import React from 'react';
import { Box, Button, chakra } from '@chakra-ui/react';

const FileUploadButton = ({ onFileSelect }) => {
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    console.log("i am uploading file")
    if (file) {
      onFileSelect(file);
    }
  };

  return (
    <Box position="relative" cursor="pointer">
      <Button
        color="white"
        rounded="md"
        _hover={{
          transform: "translateY(-2px)",
          boxShadow: "md",
          transition: "transform 0.3s ease",
          bg: "purple.600"
        }}
        bg="purple.400"
        boxShadow="lg"
        p={6}
        mt={2}
        onClick={() => document.getElementById('file-upload').click()}
      >
        Upload Course/Syllabus
      </Button>
      <chakra.input
        id="file-upload"
        type="file"
        accept="application/pdf"
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
    </Box>
  );
};

export default FileUploadButton;
