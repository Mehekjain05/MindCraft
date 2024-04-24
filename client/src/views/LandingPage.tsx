import React from 'react';
import Navbar_Landing from '../components/navbar';
import Footer from '../components/footer'
import land1 from '../assets/images/landing.png'
import feat1 from '../assets/images/language-img.jpg'
import feat2 from '../assets/images/feat2.png'
import feat3 from '../assets/images/feat3.png'
import feat4 from '../assets/images/feat4.png'
import Typewriter from 'typewriter-effect';
import Testimonials from '../components/Testimonials'
import Pricing from '../components/Pricing'
import Features from '../components/Features'

import './Landing.css'

// import Blob from '../components/Blob'
import {
  Box,
  Button,
  Flex,
  Heading,
  useColorMode,
  useColorModeValue,
  Image,
  Stack,
  Text,
  Grid
} from '@chakra-ui/react';
import '../assets/font.css';

import { Link } from 'react-router-dom';


export default function SplitScreen() {


  return (
    <div>
      <Navbar_Landing />
      <div className="absolute1">
        <div className="bg-shape1 bg-purple"></div>
      </div>
      <div className="absolute2">
        <div className="bg-shape1 bg-teal"></div>
      </div>


      <Stack minH={'95vh'} zIndex={10} direction={{ base: 'column', md: 'row' }}>
        <Flex p={8} flex={3} align={'center'} justify={'center'}>
          <Stack spacing={8} w={'full'} maxW={'85vh'}>
            <Heading fontSize={{ base: '3xl', md: '4xl', lg: '5xl' }}>
              <Text
                as={'span'}
                position={'relative'}
                color={'white'}
                px={2}
                py={2}
                className='main-heading'
                bg={'purple.500'}
              >
                MindCraft
              </Text>
              <br />
              <Text color={'purple.500'} as={'span'}>
                <Typewriter
                  options={{
                    strings: ['Learn Through AI'],
                    autoStart: true,
                    loop: true,
                  }}
                />
              </Text>
            </Heading>
            <Text textAlign={'justify'} minW={'500px'} className='content' fontSize={{ base: 'md', lg: 'lg' }}>
              MindCraft transforms education with personalized coaching, dynamic learning, and voice search, catering to students from high school to postgraduate levels. It offers quizzes, progress tracking, and downloadable notes for self-directed learning.
            </Text>
            <Stack direction={{ base: 'column', md: 'row' }} spacing={4}>
              <Link to="/login">
                <Button
                  rounded={'full'}
                  bg={useColorModeValue('purple.400', 'purple.600')}
                  color={'white'}
                  w="150px" // Set the width
                  h="70px" // Set the height
                  _hover={{
                    bg: useColorModeValue('purple.700', 'purple.900'),
                    color: useColorModeValue('white', 'white'),
                  }}
                >
                  Get Started
                </Button>
              </Link>
              <Button
                rounded={'full'}
                color={useColorModeValue('black', 'purple.600')}
                bg={useColorModeValue('gray.300', 'white')}
                w="150px" // Set the width
                h="70px" // Set the height
                _hover={{
                  bg: useColorModeValue('gray.600', 'gray.600'),
                  color: useColorModeValue('white', 'black'),
                }}
              >
                Read More
              </Button>
            </Stack>
          </Stack>
        </Flex>
        <Flex flex={2} mr={20}>
          <Image
            alt={'Login Image'}
            objectFit={'contain'}
            boxSize={{ base: '100%', md: '100%' }} // Set the desired dimensions here
            src={land1}
          />
        </Flex>
      </Stack>
      <div className="absolute3">
        <div className="bg-shape1 bg-teal"></div>
      </div>
      <div className="absolute4">
        <div className="bg-shape1 bg-purple"></div>
      </div>
      <Features/>
      {/* <Pricing/> */}
      <Testimonials/>
      <Footer />
    </div>
  );
}
