import { Box, Text, Flex, Icon, Heading } from "@chakra-ui/react";
import { ArrowUpIcon, ArrowDownIcon } from '@chakra-ui/icons';
import {
    LineChart,
    Line,
    XAxis,
    CartesianGrid,
    Tooltip,
} from "recharts";

const Dashboard = () => {
    const weeklyData = [
        { name: 'Monday', activity: 20 },
        { name: 'Tuesday', activity: 25 },
        { name: 'Wednesday', activity: 30 },
        { name: 'Thursday', activity: 27 },
        { name: 'Friday', activity: 35 },
        { name: 'Saturday', activity: 40 },
        { name: 'Sunday', activity: 30 },
    ];

    // Assuming you want to use these for the LineChart
    const title = "Daily Activity";
    const dataKey = "activity";
    const grid = true;

    return (
        <div>
            <Flex direction="row" align="center" justify="center" w="full">
                {/* Revenue Box */}
                <Box
                    w="full"
                    p={6}
                    m={4}
                    borderRadius="lg"
                    boxShadow="lg"
                    cursor="pointer"
                    backgroundColor="purple.500"
                >
                    <Text fontSize="xl" color="white">Total Courses Completed</Text>
                    <Flex mt={4} align="center">
                        <Text fontSize="2xl" fontWeight="bold">
                            
                        </Text>
                        <Text ml={4} display="flex" alignItems="center" color="white">
                            15{" "}
                            <Icon as={ArrowUpIcon} w={4} h={4} color="green.500" ml={1} />
                        </Text>
                    </Flex>
                    <Text mt={2} fontSize="md" color="white">
                        Compared to last month
                    </Text>
                </Box>

                {/* Sales Box */}
                <Box
                    w="full"
                    p={6}
                    m={4}
                    borderRadius="lg"
                    boxShadow="lg"
                    cursor="pointer"
                >
                    <Text fontSize="xl">Total Quizes Attempted</Text>
                    <Flex mt={4} align="center">
                        <Text fontSize="2xl" fontWeight="bold">
                            
                        </Text>
                        <Text ml={4} display="flex" alignItems="center">
                            48{" "}
                            <Icon as={ArrowDownIcon} w={4} h={4} color="red.500" ml={1} />
                        </Text>
                    </Flex>
                    <Text mt={2} fontSize="md" color="gray.500">
                        Compared to last month
                    </Text>
                </Box>

                {/* Cost Box */}
                <Box
                    w="full"
                    p={6}
                    m={4}
                    borderRadius="lg"
                    boxShadow="lg"
                    cursor="pointer"
                    backgroundColor="purple.500"
                >
                    <Text fontSize="xl" color="white">Max Week Spend on Course</Text>
                    <Flex mt={4} align="center">
                        <Text fontSize="2xl" fontWeight="bold">
                        </Text>
                        <Text ml={4} display="flex" alignItems="center" color="white">
                            3{" "}
                            <Icon as={ArrowUpIcon} w={4} h={4} color="green.500" ml={1} />
                        </Text>
                    </Flex>
                    <Text mt={2} fontSize="md" color="white">
                        Compared to last month
                    </Text>
                </Box>
            </Flex>
            <Box
                m={5}
                p={5}
                boxShadow="lg"
                borderRadius="lg"
                w="full"
                height="400px" // Ensure the container has a defined height
            >
                <Heading mb={1}>{title}</Heading>
                <LineChart width={1600} height={250} data={weeklyData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}    style={{
            fontSize: '22px',
        }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <Tooltip />
                    <CartesianGrid stroke="#e0dfdf" strokeDasharray="5 5" />
                    <Line type="monotone" dataKey={dataKey} stroke="#8884d8" />
                </LineChart>
            </Box>
        </div >
    );
};

export default Dashboard;
