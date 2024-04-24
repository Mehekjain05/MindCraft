import Nav from '../components/navbar';
import Footer from '../components/footer';
import Study from '../assets/images/study.jpg';
import Stud1 from '../assets/images/stud1.jpg';
import Stud2 from '../assets/images/stud2.jpg';
import Stud3 from '../assets/images/stud3.jpg';
import { useState, useEffect } from 'react';
import {
    Box,
    chakra,
    Container,
    Stack,
    Text,
    Image,
    Flex,
    VStack,
    Button,
    Heading,
    SimpleGrid,
    StackDivider,
    useColorModeValue,
    VisuallyHidden,
    List,
    Table,
    Thead,
    Tbody,
    Tfoot,
    Tr,
    Th,
    Td,
    TableCaption,
    TableContainer,
    Grid,
    Icon,
    Accordion,
    AccordionItem,
    AccordionButton,
    AccordionPanel,
    CardBody,
    CardFooter,
    Spinner,
    Center,
    Card,
    ListItem,
    ListIcon,
    OrderedList,
} from '@chakra-ui/react'
import { MdLocalShipping } from 'react-icons/md'
import { TimeIcon, CalendarIcon, EditIcon, LockIcon, BellIcon, ChevronDownIcon, StarIcon, CheckCircleIcon } from '@chakra-ui/icons';
import SimpleThreeColumns from '../components/SimpleThreeColumns';
import { useSessionCheck } from "./useSessionCheck";
import axios from 'axios';
import Slideshow from './Sildeshow';
import { NavLink } from 'react-router-dom';

export default function Simple() {
    useSessionCheck();
    const [data, setData] = useState([]);
    const [moduleData, setmoduleData] = useState({});
    const [selectedSubject, setSelectedSubject] = useState();
    const [images, setImages] = useState([]);
    const [videos, setVideos] = useState([]);
    const [othermoduleData, setothermoduleData] = useState({});
    const [isLoading, setIsLoading] = useState(true);
    const source_lang = localStorage.getItem('source_lang');

    useEffect(() => {
        const fetchData = async () => {
            const moduleid = localStorage.getItem('moduleid');
            const websearch = localStorage.getItem('websearch');
            const source_lang = localStorage.getItem('source_lang');
            try {
                const response = await axios.get(`/api/query2/course-overview/${moduleid}/${source_lang}/${websearch}`);
                setImages(response.data.images);
                setVideos(response.data.videos);
                setData(response.data.content);
                setmoduleData(response.data.module);
                setothermoduleData(response.data.other_modules)
                setSelectedSubject(response.data.content.length > 0 ? response.data.content[0] : null);
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, []);

    if (isLoading) {
        // Handle the case when subject is not defined
        return (
            <Box textAlign="center" w="205vh" height={"60vh"}>
                <Spinner size="xl" mt={"140px"} color="purple.500" />
                <Text mt={4}>Generating Content...</Text>
            </Box>
        );
    }

    const StarRating = ({ rating }) => {
        const stars = [];
        for (let i = 0; i < 5; i++) {
            stars.push(
                <Star key={i} isFilled={i < rating} />
            );
        }
        return <Flex>{stars}</Flex>;
    };

    const Star = ({ isFilled }) => (
        <StarIcon
            color={isFilled ? "yellow.500" : "gray.200"}
            boxSize={5}
            mr={1}
        />
    );
    return (
        <>
            <Nav />
            <Container maxW={'7xl'}>
                <Grid templateColumns={{ base: '1fr', md: '30% 70%' }} gap={{ base: 8, md: 20 }} py={{ base: 8, md: 14 }}>
                    <Stack spacing={20}>
                        <TableContainer gridColumn={{ base: '1 / -1', md: '1 / 2' }}>
                            <Table border="2px dashed" borderColor="gray.300">
                                <Thead>
                                    <Tr borderBottom="2px dashed" borderColor="gray.300">
                                        <Stack spacing={6} padding={6} _hover={{ transform: 'scale(1.05)' }}
                                            transition='transform 0.2s'>
                                            <Flex>
                                                <Box
                                                    borderRadius="full"
                                                    width="45px" // Adjust the size as needed
                                                    bg="black" // Set the background color of the circle
                                                    display="flex"
                                                    alignItems="center"
                                                    justifyContent="center"
                                                >
                                                    <Icon as={TimeIcon} boxSize="24px" color="white" />
                                                </Box>
                                                <Th fontSize={14}>Durations: {Object.keys(data).length/2} hours</Th>
                                            </Flex>
                                        </Stack>
                                    </Tr>
                                </Thead>
                                <Tbody>
                                    <Tr borderBottom="2px dashed" borderColor="gray.300">
                                        <Stack spacing={6} padding={6} _hover={{ transform: 'scale(1.05)' }}
                                            transition='transform 0.2s'>
                                            <Flex>
                                                <Box
                                                    borderRadius="full"
                                                    width="45px" // Adjust the size as needed
                                                    bg="red.300" // Set the background color of the circle
                                                    display="flex"
                                                    alignItems="center"
                                                    justifyContent="center"
                                                >
                                                    <Icon as={BellIcon} boxSize="24px" color="white" />
                                                </Box>
                                                <Th fontSize={14}>Language: {source_lang}</Th>
                                            </Flex>
                                        </Stack>
                                    </Tr>
                                    <Tr borderBottom="2px dashed" borderColor="gray.300" _hover={{ transform: 'scale(1.05)' }}
                                        transition='transform 0.2s'>
                                        <Stack spacing={6} padding={6}>
                                            <Flex>
                                                <Box
                                                    borderRadius="full"
                                                    width="45px" // Adjust the size as needed
                                                    bg="cyan.600" // Set the background color of the circle
                                                    display="flex"
                                                    alignItems="center"
                                                    justifyContent="center"

                                                >
                                                    <Icon as={CalendarIcon} boxSize="24px" color="white" />
                                                </Box>
                                                <Th fontSize={14}>Lectures: {Object.keys(data).length}</Th>
                                            </Flex>
                                        </Stack>
                                    </Tr>
                                    <Tr borderBottom="2px dashed" borderColor="gray.300">
                                        <Stack spacing={6} padding={6} _hover={{ transform: 'scale(1.05)' }}
                                            transition='transform 0.2s'>
                                            <Flex>
                                                <Box
                                                    borderRadius="full"
                                                    width="45px" // Adjust the size as needed
                                                    bg="purple.400" // Set the background color of the circle
                                                    display="flex"
                                                    alignItems="center"
                                                    justifyContent="center"

                                                >
                                                    <Icon as={LockIcon} boxSize="24px" color="white" />
                                                </Box>
                                                <Th fontSize={14}>Students: Max 50</Th>
                                            </Flex>
                                        </Stack>
                                    </Tr>
                                    <Tr borderBottom="2px dashed" borderColor="gray.300">
                                        <Stack spacing={6} padding={6} _hover={{ transform: 'scale(1.05)' }}
                                            transition='transform 0.2s'>
                                            <Flex>
                                                <Box
                                                    borderRadius="full"
                                                    width="45px" // Adjust the size as needed
                                                    bg="orange.400" // Set the background color of the circle
                                                    display="flex"
                                                    alignItems="center"
                                                    justifyContent="center"

                                                >
                                                    <Icon as={EditIcon} boxSize="24px" color="white" />
                                                </Box>
                                                <Th fontSize={14}>Skill Level: {moduleData.level}</Th>
                                            </Flex>
                                        </Stack>
                                    </Tr>
                                </Tbody>
                            </Table>
                        </TableContainer>
                        <Box border='1px solid black' borderRadius='md' p={4} overflow='hidden'>
                            <Stack>
                                <Heading fontSize={20} marginTop={2}>Other Modules</Heading>
                                {othermoduleData.map(module => (
                                    <Card
                                        direction={{ base: 'column', sm: 'row' }}
                                        overflow='hidden'
                                        variant='outline'
                                        _hover={{ transform: 'scale(1.05)' }}
                                        transition='transform 0.2s'
                                    >
                                        <Image
                                            objectFit='cover'
                                            maxW={{ base: '100%', sm: '100px' }}
                                            maxH={{ sm: "100px" }}
                                            src={Stud1}
                                            alt='Caffe Latte'
                                            marginTop={2}
                                            marginLeft={3}
                                        />
                                        <Stack>
                                            <CardBody>
                                                <Heading size='md'> {module.module_name}</Heading>
                                            </CardBody>

                                        </Stack>
                                    </Card>
                                ))}

                            </Stack>
                        </Box>
                    </Stack>
                    <Stack spacing={{ base: 6, md: 10 }}>
                        <Center>
                            <Slideshow images={images[0]} />
                        </Center>
                        <Box as={'header'}>
                            <Heading
                                lineHeight={1.1}
                                fontWeight={600}
                                fontSize={{ base: '2xl', sm: '4xl', lg: '5xl' }}>
                                Course Overview of {moduleData.module_name}:
                            </Heading>
                        </Box>

                        <Stack
                            spacing={{ base: 4, sm: 6 }}
                            direction={'column'}
                            divider={
                                <StackDivider borderColor={useColorModeValue('gray.200', 'gray.600')} />
                            }>
                            <VStack spacing={{ base: 4, sm: 6 }}>
                                <Text fontSize={'lg'}>
                                    {moduleData.summary}
                                </Text>
                            </VStack>

                        </Stack>
                        <Box as={'header'}>
                            <Heading
                                lineHeight={1.1}
                                fontWeight={600}
                                fontSize={{ base: '2xl', sm: '4xl', lg: '5xl' }}>
                                What You Will Learn?
                            </Heading>
                        </Box>
                        <Stack
                            spacing={{ base: 4, sm: 6 }}
                            direction={'column'}
                            align="start"
                            fontSize={17}
                            divider={
                                <StackDivider borderColor={useColorModeValue('gray.200', 'gray.600')} />
                            }
                        >
                            <VStack spacing={{ base: 4, sm: 6 }}>
                                <OrderedList>
                                    {data.map((dict, index) => (
                                        <ListItem key={index}>
                                            <ListIcon as={CheckCircleIcon} color='green.500' />
                                            {dict.subject_name}
                                        </ListItem>
                                    ))}
                                </OrderedList>
                            </VStack>
                            <SimpleThreeColumns />
                        </Stack>
                        <NavLink to="/content">
                            <Stack align="center">
                                <Button colorScheme='purple' size='lg' width={200}>
                                    Get Started
                                </Button>
                            </Stack>
                        </NavLink>
                    </Stack>

                </Grid>

            </Container>
            <Footer />
        </>
    )
}