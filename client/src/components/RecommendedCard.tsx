import React, { useState } from 'react';
import {
 Box, Text, Stack, Heading, Image, Card, CardBody, CardFooter, Button, useColorMode,
 useColorModeValue, Divider, ButtonGroup, Flex, Avatar,
 Center
} from '@chakra-ui/react';
import image1 from '../assets/cards/image1.jpg'
import image2 from '../assets/cards/image2.jpg'
import image3 from '../assets/cards/image3.jpg'
import image4 from '../assets/cards/image4.jpg'
import image5 from '../assets/cards/image5.jpg'
import image6 from '../assets/cards/image6.jpg'
import image7 from '../assets/cards/image7.jpg'
import image8 from '../assets/cards/image8.jpg'
import image9 from '../assets/cards/image9.jpg'
import image10 from '../assets/cards/image10.jpg'
import user from '../assets/images/user.jpg'
import { StarIcon } from '@chakra-ui/icons';

interface CourseCardProps {
 moduleTopic: string;
 moduleSummary: string;
}

const RecommendedCard: React.FC<CourseCardProps> = ({ moduleTopic, moduleSummary }) => {
 const [isHovered, setIsHovered] = useState(false);
 const [isFilled, setIsFilled] = useState(false); // State to manage SVG fill

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

 const handleMouseEnter = () => setIsHovered(true);
 const handleMouseLeave = () => setIsHovered(false);

 const images = [image1, image2, image3, image4, image5, image6, image7, image8, image9, image10];

 const randomIndex = Math.floor(Math.random() * images.length);
 const randomImage = images[randomIndex];

 // Function to handle SVG icon click
 const handleIconClick = () => {
    setIsFilled(!isFilled); // Toggle the fill state
 };

 return (
    <Box boxShadow='lg' rounded='md' position="relative" overflow="hidden">
      <Card onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
        <CardBody
          _hover={{
            "::before": {
              opacity: 1,
              transform: "translateX(0)",
            },
            ".learn-more-button": {
              opacity: 1,
              transform: "translateY(0)",
            },
          }}
          _before={{
            content: '""',
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            height: "310px",
            backgroundColor: "rgba(177, 156, 217, 0.5)",
            opacity: 0,
            transform: "translateX(-100%)",
            transition: "opacity 0.3s, transform 0.3s",
            zIndex: 1,
          }}
        >
          <Flex direction="column" justify="space-between" h="100%">
            <Image
              src={randomImage}
              alt='Random Image'
              borderRadius='lg'
              objectFit="cover"
              h="290px" // Set a fixed height for the image
            />
            <Stack mt='6' spacing='3'>
              <Stack spacing='3'>
                <Stack spacing='3' direction="row" justify="space-between" align="center">
                 <Heading size='md'>{moduleTopic}</Heading>
                 <StarRating rating={4} />
                </Stack>
                <Text>
                 {moduleSummary}
                </Text>
              </Stack>
              {/* Add the StarRating component here */}
            </Stack>
          </Flex>

          {/* Line that appears on hover */}
          <Box
            position="absolute"
            bottom="0"
            left="50%"
            width={isHovered ? "100%" : "0"}
            height="6px"
            backgroundColor="#B794F4"
            transform="translateX(-50%)"
            transition="width 0.5s ease, transform 0.5s ease"
          />
        </CardBody>
        <Divider />
        <CardFooter>
          <ButtonGroup spacing='2' justifyContent="center">
            <Button variant='solid' bg={'purple.400'} color={useColorModeValue('white', 'white')} _hover={{bg:useColorModeValue('purple.600', 'purple.600'), color: useColorModeValue('white', 'white'), transform: "scale(1.05)" }}>
              Get Started
            </Button>
            <Stack padding={2}>
              <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill={isFilled ? "red" : "gray"} onClick={handleIconClick} class="bi bi-heart-fill" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314" />
              </svg>
            </Stack>
          </ButtonGroup>
        </CardFooter>
      </Card>
    </Box>
 );
};

export default RecommendedCard;
