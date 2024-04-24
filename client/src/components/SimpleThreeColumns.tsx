import { ReactElement } from 'react'
import { Box, SimpleGrid, Icon, Text, Stack, Flex } from '@chakra-ui/react'
import { FcGlobe, FcFinePrint, FcHeadset } from 'react-icons/fc'

interface FeatureProps {
 title: string
 text: string
 icon: ReactElement
}

const Feature = ({ title, text, icon }: FeatureProps) => {
 return (
    <Stack>
      <Flex
        w={16}
        h={16}
        align={'center'}
        justify={'center'}
        color={'white'}
        rounded={'full'}
        bg={'gray.100'}
        mb={1}>
        {icon}
      </Flex>
      <Text fontWeight={600}>{title}</Text>
      <Text color={'gray.600'}>{text}</Text>
    </Stack>
 )
}

export default function SimpleThreeColumns() {
 return (
    <Box p={4}>
      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10}>
        <Box
          border='1px solid black'
          borderRadius='md'
          p={4}
          overflow='hidden'
          _hover={{ transform: 'scale(1.05)' }}
          transition='transform 0.2s'
        >
          <Feature
            icon={<Icon as={FcGlobe} w={10} h={10} />}
            title={'Multilingual'}
            text={
              'Course offers contents with Multilingual support enabling students to access educational materials in their preferred language'
            }
          />
        </Box>
        <Box
          border='1px solid black'
          borderRadius='md'
          p={4}
          overflow='hidden'
          _hover={{ transform: 'scale(1.05)' }}
          transition='transform 0.2s'
        >
          <Feature
            icon={<Icon as={FcFinePrint} w={10} h={10} />}
            title={'Quiz'}
            text={
              'Supports Theoretical Quiz, Application Quiz and Audio-Based Quiz to evaluate the knownledge'
            }
          />
        </Box>
        <Box
          border='1px solid black'
          borderRadius='md'
          p={4}
          overflow='hidden'
          _hover={{ transform: 'scale(1.05)' }}
          transition='transform 0.2s'
        >
          <Feature
            icon={<Icon as={FcHeadset} w={10} h={10} />}
            title={'Audio & PDFS'}
            text={
              'Generate Audios and pdf of the courses and download it for offline use'
            }
          />
        </Box>
      </SimpleGrid>
    </Box>
 )
}
