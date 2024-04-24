import React, { useState, useEffect, useRef } from 'react';
import { Input, Text, Image, Stepper, Step, StepIndicator, StepStatus, Box, Stack, StepSeparator, Heading, Flex, Textarea, Button } from '@chakra-ui/react';
import { CheckCircleIcon } from '@chakra-ui/icons';
import Nav from '../components/navbar';
import Footer from '../components/footer';
import box from '../assets/images/box.gif';
import axios from 'axios';
import { UnorderedList, ListItem, Spinner, List } from "@chakra-ui/react";
import { Editable, EditablePreview, EditableInput} from "@chakra-ui/react";
import { useNavigate } from 'react-router-dom';


const PersonalisedCourses = () => {
    const [text, setText] = useState('');
    const [text2, setText2] = useState('');
    const [inputValue, setInputValue] = useState('');
    const [descriptionValue, setDescriptionValue] = useState('');
    const [submodules, setsubModules] = useState([]);
    const [isLoadingData, setIsLoadingData] = useState(false);
    const navigate = useNavigate();

    const sendDataToAPI = async (data) => {
        try {
            setIsLoadingData(true);
            // Make POST request to your Flask API route
            const response = await axios.post('/api/query2/doc-upload', data);
            setsubModules(response.data.submodules)
            setIsLoadingData(false);
        } catch (error) {
            console.error('Error sending data:', error);
        }
    };

    const messages = [
        "Learn Machine Learning in 8 weeks",
        "Master Linear Algebra"
    ];
    const messages2 = [
        "I am School Student i want to learn about finance",
        "I am new joinee in computer science give me a begineer friendly course"
    ];
    const messageIndexRef = useRef(0);
    let index = 0;
    const [selectedFile, setSelectedFile] = useState(null);

    const handleChange = (event) => {
        setInputValue(event.target.value);
    };

    const handleDescriptionChange = (event) => {
        setDescriptionValue(event.target.value);
    };

    const handleFileChange = (e) => {
        setSelectedFile(e.target.files[0]);
    };

    const handleNextStep3 = () => {
        const formData = new FormData();
        formData.append('title', inputValue);
        formData.append('description', descriptionValue);
        formData.append('file', selectedFile);

        // Send data to Flask route using Axios
        sendDataToAPI(formData);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file) {
            setSelectedFile(file);
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
    };

    useEffect(() => {
        const timer = setInterval(() => {
            const currentMessageIndex = messageIndexRef.current;
            if (index < messages[currentMessageIndex].length) {
                setText(messages[currentMessageIndex].slice(0, index + 1));
                index++;
            } else {
                clearInterval(timer);
                setTimeout(() => {
                    index = 0;
                    messageIndexRef.current = (messageIndexRef.current + 1) % messages.length;
                    setText('');
                }, 1000);
            }
        }, 100);
        setText2(messages2[messageIndexRef.current]);
        return () => clearInterval(timer);
    }, []);

    const steps = [
        {
            title: 'Step 1', content: <div>
                <Box textAlign="center" marginTop={4}
                    style={{ width: '100%', maxWidth: '800px', margin: '0 auto' }}> {/* Increased maxWidth */}
                    <Heading size="lg" margin={7}>Enter your Course title</Heading>
                    <Input placeholder='Machine Learning' value={inputValue}
                        onChange={handleChange} size='lg' />
                    <Stack align="end" margin={5} marginBottom={45}>
                        <Button
                            colorScheme='purple'
                            size='lg'
                            width={200}
                            disabled={!text.trim()}
                            onClick={() => {
                                setActiveStep(prevStep => prevStep + 1);
                                setText('');
                            }}
                        >
                            Next
                        </Button>
                    </Stack>
                </Box>

            </div>
        },
        {
            title: 'Step 2', content: <div>
                <Box textAlign="center" marginTop={4}
                    style={{ width: '100%', maxWidth: '800px', margin: '0 auto' }}> {/* Increased maxWidth */}
                    <Heading size="lg" margin={7}>Describe your course</Heading>
                    <Textarea
                        placeholder={text}
                        value={descriptionValue}
                        onChange={handleDescriptionChange}
                        style={{
                            width: '700px', // Adjusted width to 100%
                            height: '250px',
                            padding: '10px',
                            fontSize: '1.2em',
                            color: '#999',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            resize: 'none',
                            margin: "10px"
                        }}
                    />
                    <Stack align="end" margin={5} marginBottom={45} >
                        <Flex gap={60}>
                            <Button
                                colorScheme='purple'
                                size='lg'
                                width={200}
                                disabled={!text.trim()}
                                onClick={() => {
                                    setActiveStep(prevStep => prevStep - 1);
                                    setText('');
                                }}
                            >
                                Back
                            </Button>
                            <Button
                                colorScheme='purple'
                                size='lg'
                                width={200}
                                disabled={!text.trim()}
                                onClick={() => {
                                    setActiveStep(prevStep => prevStep + 1);
                                    setText('');
                                }}
                            >
                                Next
                            </Button>
                        </Flex>
                    </Stack>
                </Box>

            </div>
        },
        {
            title: 'Step 3', content: <div>
                <Box
                    border="2px dashed"
                    borderRadius="md"
                    padding={14}
                    margin={5}
                    textAlign="center"
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                    cursor="pointer"
                    display="flex" // Add this line
                    justifyContent="center" // Add this line
                    alignItems="center" // Add this line
                    flexDirection="column" // Add this line to stack children vertically
                >
                    <Image
                        src={box} // Replace with the actual path to your GIF
                        alt="Drag and drop PDF"
                        mb={4}
                        width={250}
                        align={'center'}
                    />
                    <Input
                        type="file"
                        accept="application/pdf"
                        onChange={handleFileChange}
                        display="none"
                        id="fileInput"
                    />
                    <label htmlFor="fileInput">
                        <Text color={'blue'}>Drag and drop a PDF here or click to select a file</Text>
                        <Text color={'blue'}>Supported File Types : .pdf, .txt, .docx, .csv</Text>
                    </label>
                    {selectedFile && (
                        <Text mt={2}>Selected file: {selectedFile.name}</Text>
                    )}
                </Box>

                <Text marginBottom={5}>Note: The time to write your course will increase if you have trained our AI with additional content</Text>
                <Stack align="end" margin={5} marginBottom={45} >
                    <Flex gap={60}>
                        <Button
                            colorScheme='purple'
                            size='lg'
                            width={200}
                            disabled={!text.trim()}
                            onClick={() => {
                                setActiveStep(prevStep => prevStep - 1);
                                setText('');
                            }}
                        >
                            Back
                        </Button>
                        <Button
                            colorScheme='purple'
                            size='lg'
                            width={200}
                            disabled={!text.trim()}
                            onClick={() => {
                                handleNextStep3(); // Call the function to send data to Flask
                                setActiveStep(prevStep => prevStep + 1);
                                setText('');
                            }}
                        >
                            Next
                        </Button>
                    </Flex>
                </Stack>
            </div>
        },
        {
            title: 'Step 4', content: <div>
                <div>
                    {
                        isLoadingData ? (
                            <Box textAlign="center" height={"500px"} marginTop={4} style={{ width: '100%', maxWidth: '800px', margin: '0 auto' }}>
                                <Spinner size="xl" color="purple.500" />
                                <Text mt={4}>Loading...</Text>
                            </Box>
                        ) : (
                            <>
                                <div>
                                    <Box textAlign="center" marginTop={4} style={{ width: '100%', maxWidth: '800px', margin: '0 auto' }}>
                                        {/* Increased maxWidth */}
                                        <Heading size="lg" margin={7}>Your Generated Submodules</Heading>
                                        <List spacing={3}>
                                            {submodules.map((item, index) => (
                                                <Editable key={index} defaultValue={item} onChange={(value) => handleEdit(value, index)}>
                                                    <EditablePreview />
                                                    <EditableInput />
                                                </Editable>
                                            ))}
                                        </List>

                                        <Stack align="center" margin={5} marginBottom={45}>
                                            <Button
                                                colorScheme='purple'
                                                size='lg'
                                                width={200}
                                                disabled={!text.trim()}
                                                onClick={() => {
                                                    navigate('/pers-content');
                                                    setActiveStep(prevStep => prevStep + 1);
                                                    setText('');
                                                }}
                                            >
                                                Generate Content
                                            </Button>
                                        </Stack>
                                    </Box>
                                </div>
                            </>
                        )
                    }
                </div>
            </div>
        },
    ];

    const [activeStep, setActiveStep] = useState(1);

    return (
        <div>
            <Nav />
            <Stack>
                <Flex align="center" justify="center" width="100%" direction={'column'}>
                    <Heading as="h2" size="lg" noOfLines={1} marginTop={5}>
                        What course will you box?
                    </Heading>
                    <Stack width={700} marginTop={45}>
                        <Stepper index={activeStep} spacing={2}>
                            {steps.map((step, index) => (
                                <Step key={index} spacing={1} onClick={() => setActiveStep(index + 1)}>
                                    <StepIndicator borderRight="1px solid" borderColor="gray.300">
                                        <StepStatus
                                            complete={<CheckCircleIcon name="check" />}
                                            incomplete={<Box>{index + 1}</Box>}
                                            active={<Box>{index + 1}</Box>}
                                        />
                                    </StepIndicator>
                                    <Box flexShrink="0">
                                        <Box>{step.title}</Box>
                                        <Box>{step.description}</Box>
                                    </Box>
                                    <StepSeparator />
                                </Step>
                            ))}
                        </Stepper>
                    </Stack>


                    {steps[activeStep - 1]?.content}
                </Flex>
            </Stack>
            <Footer />
        </div>
    );
};

export default PersonalisedCourses;
