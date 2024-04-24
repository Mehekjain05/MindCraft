import React from 'react';
import { Box, Text, Button, VStack, Heading } from '@chakra-ui/react';

interface WorkingCardProps {
    initialLessonName?: string;
    initialProgress?: number;
    moduleSummary?: string; // Add this line
}

// Custom Progress Bar Component
const CustomProgressBar: React.FC<{ value: number }> = ({ value }) => {
    let progressPercentage = value;
    return (
        <Box width="100%" height="20px" bg="gray.200" borderRadius="md">
            <Box
                width={`${progressPercentage}%`}
                height="100%"
                bg="purple.400"
                borderRadius="md"
            />
        </Box>
    );
};

const WorkingCard: React.FC<WorkingCardProps> = ({
    initialLessonName = '',
    initialProgress = 0,
    moduleSummary = '', 
}) => {
    let progressPercentage = 0;
    switch(initialProgress) {
        case 1:
            progressPercentage = 30;
            break;
        case 2:
            progressPercentage = 60;
            break;
        default:
            progressPercentage = 0; // Default to 0 if value is neither 1 nor 2
    }
    const [lessonName, setLessonName] = React.useState(initialLessonName);
    const [progress, setProgress] = React.useState(progressPercentage);
    
    const handleLessonNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setLessonName(event.target.value);
    };

    // Example function to update progress
    const updateProgress = (newProgress: number) => {
        setProgress(newProgress);
    };

    return (
        <Box bg="white" p={4} borderRadius="md" boxShadow="md" margin={6} width={['100%', '90%', '80%', '450px']}
        height="90%">

            <VStack spacing={4} align="start">
                <Heading size="md">Jump back in</Heading>
                <Text>Course {progress}% Completed</Text>
                <CustomProgressBar value={progress} />
                <Text>Current Lesson: {lessonName}</Text>
                <Text>Module Summary: {moduleSummary}</Text> 
                <Button colorScheme='purple'>Continue Learning</Button>
            </VStack>
        </Box>
    );
};

export default WorkingCard;
